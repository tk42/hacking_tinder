#!/usr/bin/env bash
pip install -r requirements.txt
. ./setenv.sh
export LANG='ja_JP.UTF-8'
export LC_ALL='ja_JP.UTF-8'
python3 hacking_tinder.py ${FACEBOOK_AUTH_TOKEN} ${FACEPP_API_KEY} ${FACEPP_API_SECRETKEY}