#!/bin/sh
easy_install pip&&pip install cymysql
python -o *.py&&rm -rf *.py