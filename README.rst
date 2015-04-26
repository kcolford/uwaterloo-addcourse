===================
UWaterloo AddCourse
===================
:Info: Documentation for the UWaterloo AddCourse package.
:Author: Kieran Colford

This python package allows one to easily interact with the University
of Waterloo's QUEST_ system to easily add a course.

.. _QUEST: https://uwaterloo.ca/quest/

.. note:: Currently only classes that have one tutorial section can be
   added.  Support for tutorial-less classes is in the works.

Usage
=====

There are two ways to use this API: the command line and the python
interpreter.

Command Line
------------

To add a class from the command line, simply invoke the helper script
like so::

  user@computer:~/$ addcourse
  Desired Course: cs246
  QUEST ID: jsmith
  Password: 
  ...

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


