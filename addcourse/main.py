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


"""The main routine used by the program."""


from .browser import QuestBrowser
from . import cls_numbers
import getpass
import readline
import logging


def main():
    """Main function."""

    logging.getLogger().addHandle(logging.StreamHandler())

    user = input('QUEST ID: ')
    password = getpass.getpass('Password: ')
    QuestBrowser(user, password).run(cls_numbers)
