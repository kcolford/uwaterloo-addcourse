#!/usr/bin/env python

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


"""Repeatedly ask QUEST to add you into a particular course."""


import urllib2
import urllib
import logging
import getpass
import itertools
import tempfile
import webbrowser
import time
import re
try:
    import readline
except ImportError:
    pass
import bs4


__author__ = 'Kieran Colford'
__license__ = 'GPLv3+'


class QuestException(Exception):

    """An exception thrown by QuestBrowser's methods."""

    pass


class QuestBrowser:

    """An opener for browsing QUEST."""

    proto = 'https'
    host = 'quest.pecs.uwaterloo.ca'
    req = None
    register_repeat_count = 2

    def __init__(self, questid, password=None):
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPSHandler())
        self.opener.add_handler(urllib2.HTTPRedirectHandler())
        self.opener.add_handler(urllib2.HTTPCookieProcessor())

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
                req.data = urllib.urlencode(self.data)
                self.data = None

        f = self.open(req)
        self.page = f.read()
        f.close()

        if req is self.req:
            self.req = None

        self.page = bs4.BeautifulSoup(self.page)

        return self.page

    def make_request(self, page, query={}):
        """Make a Request object for a QUEST page."""

        self.data = {}
        self.req = urllib2.Request(
            self.proto + '://' + self.host + page +
            ('?' + urllib.urlencode(query) if query != {} else ''))

    def add_header(self, key, val):
        """Add key and val to the header of self.req."""

        self.req.add_header(key, val)

    def add_form(self, key, val):
        """Add key=val to the data field of self.req."""

        if not isinstance(self.data, dict):
            raise Exception(
                "Need to call self.make_request before calling self.add_form.")
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(val, str):
            val = str(val)
        self.data[key] = val

    def add_forms(self, d):
        """Add key, value pairs from d to self.data."""

        for k, v in d.items():
            self.add_form(k, v)

    def login(self, password):
        """Login to QUEST."""

        assert password is not None

        self.make_request('/psc/AS/', {'cmd': 'login',
                                       'languageCd': 'ENG'})
        self.add_forms({'userid': self.questid,
                        'pwd': password,
                        'httpPort': '',
                        'timezoneOffset': '240',
                        'Submit': 'Sign+in'})
        self.get_page()

        if self.page.find(text=invalid_id_pass_msg):
            raise QuestException(invalid_id_pass_msg)

    def get_add(self):
        """Go to the enrollment page."""

        self.do_action('DERIVED_SSS_SCR_SSS_LINK_ANCHOR3')

        add_link = self.page.find(text='add').parent
        log.debug("add link is %s", add_link)
        self.make_request(add_link['href'])
        self.get_page()

        self.do_action('DERIVED_SSS_SCT_SSR_PB_GO',
                       {'SSR_DUMMY_RECV1$sels$0': "1"})

    def setup_post(self):
        """Setup a POST request from QUEST."""

        for n in self.page.find_all(name='input', attrs={'type': 'hidden'}):
            self.add_form(n['name'], n['value'])

        log.debug("%s", str(self.data))

    def do_action(self, action, d={}):
        """Do a POST action on the add class page."""

        self.make_request(enroll_add_page)
        self.setup_post()
        self.add_form('ICAction', action)
        self.add_forms(d)
        self.get_page()

    def register_class(self, classno, tutno=0):
        """Register into the class classno."""

        self.get_add()

        self.do_action('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$',
                       {'DERIVED_REGFRM1_CLASS_NBR': classno})

        if not self.page.find(text=has_class_message):
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

        if len(self.page.find_all(name='img', attrs={'alt': 'Error'})) >= 2:
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

    def run(self, course):
        """Keep requesting the class we want from QUEST."""

        if isinstance(course, str):
            class_numbers = numbers(course)
        elif isinstance(course, list):
            class_numbers = [int(n) for n in course]
        else:
            raise TypeError("course is not a list or str")

        self.get_add()
        log.info("Navigated to Add page, begining reqests.")

        for i in itertools.count():
            for cls in class_numbers:
                self.register_class(cls)
                try:
                    for j in range(self.register_repeat_count):
                        if self.get_registered_class():
                            log.info("Attempt %s on class %s Succeeded.",
                                     i * self.register_repeat_count + j + 1,
                                     cls)
                            preview_page(self.page)
                            return
                        else:
                            log.info("Attempt %s on class %s Failed.",
                                     i * self.register_repeat_count + j + 1,
                                     cls)
                finally:
                    self.clear_class()


def preview_page(html):
    """Preview the HTML code html in your browser."""

    with tempfile.NamedTemporaryFile(mode='w+t') as f:
        f.write(str(html))
        f.flush()
        webbrowser.open('file://' + f.name)
        time.sleep(5)


def nearest_term(t=time.time()):
    """Return the number for the nearest term."""

    t = time.localtime(t)
    y = t.tm_year % 100
    m = int((t.tm_mon + 2) / 4) * 4 + 1
    return 1000 + y * 10 + m


def numbers(course):
    """Return a list of class numbers corresponding to course."""

    subject, number = re.findall(r'[a-zA-Z]+|[0-9]+', course)
    query = {'level': 'under',
             'sess': nearest_term(),
             'subject': subject.upper(),
             'cournum': number}

    f = urllib2.urlopen(course_query_url, urllib.urlencode(query))
    a = bs4.BeautifulSoup(f.read())
    f.close()

    return [int(n.parent.previous)
            for n in a.findAll(text=re.compile('LEC'))]


def addcourse(user, password, course):
    """Run the QuestBrowser and get into the course we need."""

    try:
        QuestBrowser(user, password).run(course)
    except QuestException as e:
        log.exception(e.message)
        raw_input("Press Enter to continue...")
        exit(1)


def main():
    """Main function."""

    course = raw_input('Desired Course: ')
    user = raw_input('QUEST ID: ')
    password = getpass.getpass('Password: ')
    addcourse(user, password, course)

log = logging.getLogger('addcourse')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

has_class_message = 'This class is already in your Shopping Cart.  Try another.'
enroll_add_page = '/psc/AS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL'
invalid_id_pass_msg = 'Your User ID and/or Password are invalid.'
course_query_url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
