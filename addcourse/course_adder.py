# Add the course we want.

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


"""Class to add the courses we want."""


import itertools
from .class_numbers import numbers
from .addpage import AddPage
from .preview import preview_page


class AddCourse(AddPage):
    """Add a course."""

    def register_class(self, classno, tutno=0):
        """Register into the class classno."""

        self.do_action('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$',
                       {'DERIVED_REGFRM1_CLASS_NBR': classno})

        if self.page.find(text=has_class_message):
            return
    
        if self.page.find(text=select_tut_message):
            self.register_tutorial(tutno)

    def register_tutorial(self, tutno=0):
        """Register into tutorial tutno."""
        
        if tutno != 0:
            if not isinstance(tutno, str):
                tutno = str(tutno)
            node = self.page.find(text=tutno)
            nodekey = node.parent['id'].split('$')[-1]
        else:
            node = self.page.find_all(name='img', attrs={'alt': 'Open'})[1]
            nodekey = node.parent.parent['id'].split('$')[-1]
        self.do_action('DERIVED_CLS_DTL_NEXT_PB',
                       {'SSR_CLS_TBL_R1$sels$0': nodekey})

    def get_registered_class(self, display_page_on_fail=False):
        """Try to get into the class we've registered into."""

        self.do_action('DERIVED_CLS_DTL_NEXT_PB$280$',
                       {'DERIVED_CLS_DTL_CLASS_PRMSN_NBR$118$': ""})

        self.do_action("DERIVED_REGFRM1_LINK_ADD_ENRL$82$")

        self.do_action("DERIVED_REGFRM1_SSR_PB_SUBMIT")

        if len(self.page.find_all(name='img', attrs={'alt': 'Error'})) >= 2:
            if display_page_on_fail:
                print self.page
            self.do_action('DERIVED_REGFRM1_SSR_LINK_STARTOVER')
            return False
        else:
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
        print "Navigated to Add page, begining reqests."

        for i in itertools.count():
            for cls in class_numbers:
                self.register_class(cls)
                try:
                    for j in range(repeat):
                        if self.get_registered_class():
                            print "Attempt", i * repeat + j + 1, "on class", cls, "Succeeded."
                            preview_page(self.page)
                            return
                        else:
                            print "Attempt", i * repeat + j + 1, "on class", cls, "Failed."
                finally:
                    self.clear_class()


def addcourse(user, password, course):
    """Run the QuestBrowser and get into the course we need."""

    try:
        AddCourse(user, password).run(course)
    except Error as e:
        print >> sys.stderr, e
        raw_input("Press Enter to continue...")
        exit(1)


has_class_message = 'This class is already in your Shopping Cart.  Try another.'
select_tut_message = 'Select TUT - Tutorial section (Required):'
repeat = 2
