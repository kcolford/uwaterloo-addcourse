# Interact with the QUEST course page.

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


"""Class that interacts with the QUEST course add page."""


import re
from .browser import QuestBrowser


class AddPage(QuestBrowser):
    """Interact with the course add page."""

    def get_add(self):
        """Go to the enrollment page."""

        # Select the enroll page.
        self.do_action('DERIVED_SSS_SCR_SSS_LINK_ANCHOR3')

        # Select the add tab.
        add_link = self.page.find(text='add').parent
        self.make_request(add_link['href'])
        self.get_page()

        # Select the upcomming term if the option is given.
        t = self.page.find(text=term_regex)
        if t and t.parent.name == 'span':
            self.do_action('DERIVED_SSS_SCT_SSR_PB_GO',
                           {'SSR_DUMMY_RECV1$sels$0': "1"})

    def setup_post(self):
        """Setup a POST request from QUEST."""

        for n in self.page.find_all(name='input', attrs={'type': 'hidden'}):
            self.add_form(n['name'], n['value'])

    def do_action(self, action, d={}):
        """Do a POST action on the add class page."""

        self.make_request(enroll_add_page)
        self.setup_post()
        self.add_form('ICAction', action)
        self.add_forms(d)
        self.get_page()


enroll_add_page = '/psc/AS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL'
term_regex = re.compile(r'^(Winter|Spring|Fall) [[:digit:]]{4}$')
