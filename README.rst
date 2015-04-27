===================
UWaterloo AddCourse
===================

This python package allows one to easily interact with the University
of Waterloo's QUEST_ system to easily add
a course.


Install
=======

The Repository_
---------------

You can install this package from source using::

  git clone https://github.com/kcolford/uwaterloo-addcourse.git
  cd uwaterloo-addcourse
  python setup.py install

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

For command line arguments, see ``addcourse --help``.

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
<http://www.gnu.org/licenses/>.


Credits
=======

| Mark Petrick, for the support that inspired this project.

.. _QUEST: https://uwaterloo.ca/quest/
.. _PyPi: https://pypi.python.org/
.. _Repository: https://github.com/kcolford/uwaterloo-addcourse
.. _`PyPi page`: https://pypi.python.org/pypi/uwaterloo-addcourse 
