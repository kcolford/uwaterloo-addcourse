# Copyright (C) 2015 Kieran Colford
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.


"""The browser that interacts with QUEST."""


from .error import QuestException
import bs4
import urllib.request, urllib.parse, urllib.error
import itertools
import logging


class QuestBrowser:
    """An opener for browsing QUEST."""

    proto = 'https'
    host = 'quest.pecs.uwaterloo.ca'
    req = None
    password = None

    has_logged_in = False    

    def __init__(self, questid, password=None):
        self.opener = urllib.request.build_opener()
        self.opener.add_handler(urllib.request.HTTPSHandler())
        self.opener.add_handler(urllib.request.HTTPRedirectHandler())
        self.opener.add_handler(urllib.request.HTTPCookieProcessor())

        self.questid = questid.upper()
        
        if password is not None:
            self.login(password)

    def open(self, req):
        """Open a request req to QUEST via self.opener."""

        if isinstance(req.data, str):
            req.data = req.data.encode('ascii')
        return self.opener.open(req)

    def add_data(self, data):
        """Add data to self.req."""

        if self.req is None:
            raise QuestException("request cannot be None")
        self.req.data = data

    def get_page(self, req=None):
        """Return a BeautifulSoup instance for url."""

        if req is None:
            if self.req is None:
                raise QuestException("request cannot be None")
            req = self.req
            if self.data:
                req.data = urllib.parse.urlencode(self.data)
                self.data = None

        f = self.open(req)
        self.page =  f.read()
        f.close()

        if req is self.req:
            self.req = None

        self.page = bs4.BeautifulSoup(self.page)
            
        return self.page;

    def make_request(self, page, query={}):
        """Make a Request object for a QUEST page."""

        self.data = {}
        self.req = urllib.request.Request(
            self.proto + '://' + self.host + page +
            ('?' + urllib.parse.urlencode(query) if query != {} else ''))
        return self.req

    def add_header(self, key, val):
        """Add key and val to the header of self.req."""

        self.req.add_header(key, val)

    def add_form(self, key, val):
        """Add key=val to the data field of self.req."""

        if not isinstance(self.data, dict):
            raise QuestException("Need to call self.make_request before calling self.add_form.")
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(val, str):
            val = str(val)
        self.data[key] = val

    def add_forms(self, d):
        """Add key, value pairs from d to self.data."""

        for k, v in list(d.items()):
            self.add_form(k, v)

    invalid_id_pass_msg = 'Your User ID and/or Password are invalid.'

    def login(self, password=None):
        """Login to QUEST."""

        if self.password is None:
            self.password = password

        if password is None:
            password = self.password

        assert password is not None

        if self.has_logged_in:
            return self

        self.make_request('/psc/AS/', {'cmd': 'login', 
                                       'languageCd': 'ENG'})
        self.add_forms({'userid': self.questid,
                        'pwd': password,
                        'httpPort': '',
                        'timezoneOffset': '240',
                        'Submit': 'Sign+in'})
        self.get_page()

        if self.page.find(text=self.invalid_id_pass_msg):
            raise QuestException(self.invalid_id_pass_msg)
        
        self.has_logged_in = True

        return self

    def find(self, idval='', attrs={}, **kwargs):
        """Return the element with id=idval."""

        if not isinstance(self.page, bs4.BeautifulSoup):
            self.page = bs4.BeautifulSoup(self.page)

        out = self.page.find(attrs={'id': idval}.update(attrs), **kwargs)
        if out is None:
            raise QuestException("could not find matching element in page")
        return out

    def get_page_dict(self, uri, d):
        self.make_request(uri + '?' +  urllib.parse.urlencode(d))
        self.get_page()

    enroll_add_page = '/psc/AS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL'

    has_added = False

    def get_add(self):
        """Go to the enrollment page."""

        if self.has_added:
            return

        self.do_action('DERIVED_SSS_SCR_SSS_LINK_ANCHOR3')
        
        add_link = self.page.find(text='add').parent
        log.debug("add link is %s", add_link)
        self.make_request(add_link['href'])
        self.get_page()

        self.do_action('DERIVED_SSS_SCT_SSR_PB_GO',
                       {'SSR_DUMMY_RECV1$sels$0':"1"})

        self.has_added = True

    def setup_post(self):
        """Setup a POST request from QUEST."""

        for n in self.page.find_all(name='input', attrs={'type': 'hidden'}):
            self.add_form(n['name'], n['value'])

        log.debug("%s", str(self.data))

    def do_action(self, action, d={}):
        """Do a POST action on the add class page."""

        self.make_request(self.enroll_add_page)
        self.setup_post()
        self.add_form('ICAction', action)
        self.add_forms(d)
        self.get_page()

    has_class_message = 'This class is already in your Shopping Cart.  Try another.'

    def register_class(self, classno, tutno=0):
        """Register into the class classno."""

        self.get_add()

        self.do_action('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$',
                       {'DERIVED_REGFRM1_CLASS_NBR': classno})

        if not self.page.find(text=self.has_class_message):
            if tutno != 0:
                if not isinstance(tutno, str):
                    tutno = str(tutno)
                node = self.page.find(text=tutno)
                nodekey = node.parent['id'].split('$')[-1]
            else:
                node = self.page.find_all(name='img', attrs={'alt': 'Open'})[1]
                nodekey = node.parent.parent['id'].split('$')[-1]
            log.debug("node key chosen was %s", nodekey)
            self.do_action('DERIVED_CLS_DTL_NEXT_PB',
                           {'SSR_CLS_TBL_R1$sels$0': nodekey})

    def get_registered_class(self, display_page_on_fail=False):
        """Try to get into the class we've registered into."""

        self.do_action('DERIVED_CLS_DTL_NEXT_PB$280$',
                       {'DERIVED_CLS_DTL_CLASS_PRMSN_NBR$118$': ""})

        self.do_action("DERIVED_REGFRM1_LINK_ADD_ENRL$82$")

        self.do_action("DERIVED_REGFRM1_SSR_PB_SUBMIT")

        if len(self.page.find_all(name='img', attrs={'alt':'Error'})) >= 2:
            log.debug("attempt failed")
            if display_page_on_fail:
                log.info(self.page)
            self.do_action('DERIVED_REGFRM1_SSR_LINK_STARTOVER')
            return False
        else:
            log.debug("Success")
            return True

    def get_class(self, classno, tutno=0, display_page_on_fail=False):
        """Attempt to register into a class with class number classno."""
        
        self.get_add()
        self.register_class(classno, tutno)
        return self.get_registered_class(display_page_on_fail)        
        
    def clear_class(self):
        """Clear the class we have saved."""

        self.do_action('P_DELETE$0')

    register_repeat_count = 3

    def run(self, class_numbers):
        """Keep requesting the class we want from QUEST."""

        class_numbers = [int(cls) for cls in class_numbers]

        self.get_add()
        log.info("Navigated to Add page, begining reqests.")

        for i in itertools.count():
            for cls in class_numbers:
                self.register_class(cls)
                for j in range(self.register_repeat_count):
                    if self.get_registered_class():
                        log.info("Attempt %s on class %s succeeded.",
                                 i * self.register_repeat_count + j + 1,
                                 cls)
                        preview_page(self.page)                            
                        return
                    else:
                        log.info("Attempt Failed.")
                self.clear_class()

log = logging.getLogger('addcourse.browser')
