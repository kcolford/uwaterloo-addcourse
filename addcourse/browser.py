# QuestBrowser class

# Copyright (C) 2015 Kieran Colford
#
# This file is part of UWaterloo-AddCourse.
#
# UWaterloo-AddCourse is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# UWaterloo-AddCourse is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UWaterloo-AddCourse.  If not, see
# <http://www.gnu.org/licenses/>.


"""The QuestBrowser class that manages interactions with QUEST."""

import urllib
import urllib2
import bs4
from .error import *


class QuestBrowser:

    """An opener for browsing QUEST."""

    req = None

    def __init__(self, questid, password):
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPSHandler())
        self.opener.add_handler(urllib2.HTTPRedirectHandler())
        self.opener.add_handler(urllib2.HTTPCookieProcessor())

        self.questid = questid.upper()

        self.login(password)

    def open(self, req):
        """Open a request req to QUEST via self.opener."""

        if isinstance(req.data, str):
            req.data = req.data.encode('ascii')
        return self.opener.open(req)

    def add_data(self, data):
        """Add data to self.req."""

        if self.req is None:
            raise Error("request cannot be None")
        self.req.data = data

    def get_page(self, req=None):
        """Return a BeautifulSoup instance for url."""

        if req is None:
            if self.req is None:
                raise Error("request cannot be None")
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
            proto + '://' + quest_url + page +
            ('?' + urllib.urlencode(query) if query != {} else ''))

    def add_header(self, key, val):
        """Add key and val to the header of self.req."""

        self.req.add_header(key, val)

    def add_form(self, key, val):
        """Add key=val to the data field of self.req."""

        if not isinstance(self.data, dict):
            raise Error(
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
            raise BadLogin(invalid_id_pass_msg)


proto = 'https'
quest_url = 'quest.pecs.uwaterloo.ca'
invalid_id_pass_msg = 'Your User ID and/or Password are invalid.'
