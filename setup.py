#!/usr/bin/env python

from setuptools import *
from addcourse.version import __version__

setup(
    name='uwaterloo-addcourse',
    version=__version__,
    author='Kieran Colford',
    author_email='colfordk@gmail.com',
    url='https://github.com/kcolford/uwaterloo-addcourse',
    license='GPLv3+',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'addcourse = addcourse:main',
        ],
    },
    install_requires=[
        'beautifulsoup4>=4.2.0',
    ],
)
