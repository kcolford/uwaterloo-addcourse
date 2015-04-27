#!/usr/bin/env python

"""Package for easily adding a course on UWaterloo's QUEST."""

from setuptools import *
from addcourse.version import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='uwaterloo-addcourse',
    version=__version__,
    author='Kieran Colford',
    author_email='colfordk@gmail.com',
    url='https://github.com/kcolford/uwaterloo-addcourse',
    license='GPLv3+',
    description=__doc__,
    long_description=long_description,
    keywords=[
        'uwaterloo',
        'addcourse',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms=['Any'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'addcourse = addcourse.main:main',
        ],
    },
    setup_requires=[
        'xdistutils>=0.2',
    ],
    install_requires=[
        'beautifulsoup4>=4.2.0',
    ],
    use_2to3=True,
)
