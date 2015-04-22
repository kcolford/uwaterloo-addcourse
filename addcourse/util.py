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


"""Utility functions used elsewhere in the package."""


import tempfile
import os


def preview_page(html):
    """Preview the HTML code html in your browser."""

    with tempfile.NamedTemporaryFile(mode='w+t') as f:
        f.write(str(html))
        f.flush()
        os.system("firefox {}".format(f.name))
        os.sleep(10)
