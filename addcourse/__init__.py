"""Repeatedly ask QUEST to add you into a particular course."""

# Expose metadata.
from .version import (
    __author__,
    __version__,
    __credits__,
)

def addcourse(user, password, classlist):
    """Repeatedly query QUEST to add classes from classlist until one of
    them works.

    """

    from .course_adder import addcourse as _addcourse
    return _addcourse(user, password, classlist)

def numbers(course):
    """Query uwaterloo.ca for a list of class numbers that correspond to
    the lecture sections of course.

    """

    from .class_numbers import numbers as _numbers
    return _numbers(course)
