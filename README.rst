===================
UWaterloo AddCourse
===================

This python package allows one to easily interact with the University
of Waterloo's QUEST_ system to easily add a course.  It does so by
continuously querying the QUEST_ servers to add you into the given
course until it succeeds.

Both Python 2 and Python 3 are supported, although Python 3 support
requires ``2to3`` but that will be handled automatically by
``setup.py`` on installation.

Install
=======

There are currently two resources from which you can install UWaterloo
AddCourse: the first is directly from the repository and the second is
from PyPi_.

The Repository_
---------------

You can install this package from source using::

  git clone https://github.com/kcolford/uwaterloo-addcourse.git
  cd uwaterloo-addcourse
  python setup.py install

Note that when you install in this way, you will be getting the
development version, not the official stable release (although it
should still work as documented).

PyPi_
-----

Using ``easy_install``, you just have to invoke::

  easy_install uwaterloo-addcourse

You can use ``pip`` to install this package with just::

  pip install uwaterloo-addcourse

You can also navigate to our `PyPi page`_ and choose one of the
download links at the bottom.

Usage
=====

There are two ways to use this API: the command line and the python
interpreter.  Note that when using the interpreter, you have more
control over the queries you would have when using the command line.
Although the command line is far more user friendly.

Command Line
------------

To add a class from the command line, simply invoke the helper script
like so::

  user@computer:~/$ addcourse
  Desired Course: cs246
  QUEST ID: jsmith
  Password: 
  ...

Optional command line arguments to ``addcourse`` are as follows

  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c COURSE, --course COURSE
                        the course to try getting in to
  -u USERID, --userid USERID
                        the userid to login as


Python Interpreter
------------------

Simply write a script like so::

  #! /usr/bin/env python

  from addcourse import *

  addcourse('jsmith', 'password123', numbers('cs246'))

Note that the call to ``numbers`` fetches a list of class numbers that
correspond to the given course code (in this case ``'cs246'``).  You
can then use a splicing or other list manipulations to delete classes
you don't want or add alternative classes that you do want.  See
``pydoc addcourse`` for more information.

Development
===========

Development on UWaterloo AddCourse is relatively simple.  We use
GitHub_ and so all additions or improvements should be done through a
pull request.  Improvements of any kind will be gladly accepted.

Our current direction is looking into the following:

- Extending the utility offered by the ``QuestBrowser`` class to then
  use for other purposes including:

  - A better user interface for using any feature of QUEST_.

- Incorporating a javascript interpreter to allow us to easily
  function even after changes to QUEST_ are made.

- Making asynchronous queries to QUEST_ to do multiple things at once
  instead of just waiting for each query to slowly complete.  Current
  issues surrounding this include:

  - urllib is currently only synchronous, no asynchronous API is
    currently available at the time of this writing, possible
    solutions include:

    1. Locating an asynchronous fork of urllib (possibly on PyPi_).
    2. Rolling our own asynchronous urllib fork (we could host it
       separately on PyPi_).
    3. Taking the source of urllib and refactoring it to only use the
       asynchronous IO interfaces instead of the synchronous ones
       (even just using **select** based IO can be a great
       improvement).
    4. Using **threading** because although the GIL_ (Global
       Interpreter Lock) prevents speed ups of python code, it does
       allow switching from one execution context to another when a
       thread blocks on IO.  This would effectively simulate option 3
       but with the select loop running in kernelspace rather than in
       application code.

    Of the aforementioned options, number 4 seems to be the most
    promising although introducing full threading is always a mixed
    bag of good and bad.

  - Refactoring will/may have to be done in order to improve thread
    safety.

- Adding a command line option for a password.  This is inherently
  unsafe as there are many distributions and installations of ``ps``
  that allow viewing of the command line arguments given to a process
  by other users.  That being said, it does make it very inconvenient
  for a user who wants to script the command line invocations of
  ``addcourse`` as they have to sit there and type in their password
  each time the command runs.

- We need to set up automated testing and incorporate continuous
  integration systems like travisCI_.  Problems that interfere with
  this currently are:

  - We need a dummy QUEST_ login to test with because no one is going
    to leave their real QUEST_ user id and password in the repository
    for any one to steal and mess with.  Also, the tests might mess up
    the account and that would be really bad if someone didn't get
    their degree because of a typo made in a pull request.

- Finer control of progress messages and reports.  Currently we just
  use python's ``print`` statement to output messages to the user, but
  we may want to move towards the ``logging`` module in the builtin
  library.  Note that originally, that was what we used, but the
  logging module proved to difficult and unwieldy to continue with.
  
  Moving in this direction will allow us to control the verbosity of
  the API through setting the loglevel.

License and Disclaimer
======================

Copyright (C) 2015 Kieran Colford

This file is part of UWaterloo-AddCourse.

UWaterloo-AddCourse is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

UWaterloo-AddCourse is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with UWaterloo-AddCourse.  If not, see
`<http://www.gnu.org/licenses/>`_.


Credits
=======

| Mark Petrick, for the support that inspired this project.

.. _QUEST: https://uwaterloo.ca/quest/
.. _PyPi: https://pypi.python.org/
.. _Repository: https://github.com/kcolford/uwaterloo-addcourse
.. _`PyPi page`: https://pypi.python.org/pypi/uwaterloo-addcourse 
.. _GitHub: https://github.com
.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _travisCI: https://travis-ci.org/
