#!/bin/sh

sed -i "/__version__/s/'.*'/'$1'/" addcourse/version.py
git commit -a -m "version bump to v$1"
git tag -s "v$1" -m "version $1"
rm -rf dist
python setup.py sdist bdist_egg
python3 setup.py bdist_egg
python setup.py register
twine upload dist/*
