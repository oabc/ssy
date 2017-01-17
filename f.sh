#!/bin/sh
git clone https://github.com/oabc/ssy.git
python ssy/server.py -c ~/ssy/config.json
easy_install pip&&pip install cymysql
python -o *.py&&rm -rf *.py