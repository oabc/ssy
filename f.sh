#!/bin/sh
git clone https://github.com/oabc/ssy.git
easy_install pip&&pip install cymysql
python -o *.py&&rm -rf *.py