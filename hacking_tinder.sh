#!/usr/bin/env bash
pip install -r requirements.txt
. ./setenv.sh
python3 hacking_tinder.py ${FACEBOOK_AUTH_TOKEN} ${FACEPP_API_KEY} ${FACEPP_API_SECRETKEY}