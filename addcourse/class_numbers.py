# Module for looking at class numbers.

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


import urllib
import urllib2
import re
import time
import bs4

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


course_query_url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
