# Main method.

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


"""The main method for this package."""

import argparse
import getpass
try:
    import readline
except ImportError:
    pass
from .course_adder import addcourse
from . import __version__


def main():
    """Main function."""

    descr = """Repeatedly ask QUEST to add you into a particular course."""
    epi = """Report Bugs to the bug list on our github page at:
    <https://github.com/kcolford/uwaterloo-addcourse/issues>"""

    parser = argparse.ArgumentParser(
        prog='addcourse',
        description=descr,
        epilog=epi,
        fromfile_prefix_chars='@',
    )
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-c', '--course', action='store',
                        help='the course to try getting in to')
    parser.add_argument('-u', '--userid', action='store',
                        help='the userid to login as')

    args = parser.parse_args()

    course = args['course']
    if not course:
        course = raw_input('Desired Course: ')
    user = args['userid']
    if not user:
        user = raw_input('QUEST ID: ')
    password = getpass.getpass('Password: ')
    addcourse(user, password, course)
