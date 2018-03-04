# -*- coding: utf-8 -*-
import unittest
import sys
import requests
from hacking_tinder.main.access_token import AccessToken

DEBUG_URL = "https://developers.facebook.com/tools/debug/accesstoken"
TR_NEVER = '<tr><td><span class="_c24 _2iem">Expires</span></td>' \
           + '<td><span class="_c24 _2iem"><span>Never</span></span></td></tr>'

at = None


class TestAccessToken(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.at = at

    def test_return_not_none(self):
        self.assertIsNotNone(at.access_token)

    # TODO: implement to assert the token will be never expired.
    # API: https://developers.facebook.com/docs/graph-api/reference/v2.12/debug_token
    # Debugger: https://developers.facebook.com/tools/debug/accesstoken/
    # def test_get_never_expire_token(self):
    #     res = requests.get(DEBUG_URL, params={"access_token": at.access_token, "version": "v2.12"})
    #     print(res.content.decode())
    #     self.assertTrue(TR_NEVER in res.content.decode())


if __name__ == '__main__':
    if len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
        sys.argv = [sys.argv[0]]
    else:
        raise ValueError("Both FACEBOOK_EMAIL and FACEBOOK_PASSWORD should be specified.")
    at = AccessToken(email, password)
    unittest.main()
