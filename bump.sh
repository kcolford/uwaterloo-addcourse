#!/bin/sh

sed -i "/__version__/s/'.*'/'$1'/" addcourse/version.py
git commit -a -m "version bump to v$1"
git tag -s "v$1"
