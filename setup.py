#!/usr/bin/env python

from setuptools import *

setup(
    name='uwaterloo-addcourse',
    version='0.1.1',
    author='Kieran Colford',
    author_email='colfordk@gmail.com',
    url='https://github.com/kcolford/uwaterloo-addcourse',
    license='GPLv3+',
    packages=['addcourse'],
    entry_points={
        'console_scripts': [
            'addcourse = addcourse:main',
        ],
    },
    install_requires=[
        'beautifulsoup4>=4.2.0',
    ],
)
