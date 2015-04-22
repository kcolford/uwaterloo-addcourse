#!/usr/bin/env python3

from setuptools import *

setup(
    name='uwaterloo-addcourse', version='0.0.1', license='GPLv3+',

    author='Kieran Colford', author_email='colfordk@gmail.com',

    description=("A script to add the courses you want from QUEST."),
    keywords=['uwaterloo',
              'course',
              'courses',
          ],

    packages=find_packages(),
    entry_points={'console_scripts': ['addcourse = addcourse.main:main']},

    platforms=['Any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],

    requires=['beautifulsoup4'],
)
