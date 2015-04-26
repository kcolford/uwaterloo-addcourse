# Previewing HTML code in browser.

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


import tempfile
import time
import webbrowser


def preview_page(html):
    """Preview the HTML code html in your browser."""

    with tempfile.NamedTemporaryFile(mode='w+t') as f:
        f.write(str(html))
        f.flush()
        webbrowser.open('file://' + f.name)
        time.sleep(5)

