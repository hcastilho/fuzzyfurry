#! /usr/bin/env bash

source $(which virtualenvwrapper.sh)
mkvirtualenv -p /usr/bin/python2.7 fuzzyfurry

#pip install -r requirements/common.txt
pip install -r requirements/development.txt
