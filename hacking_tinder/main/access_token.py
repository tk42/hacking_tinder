# -*- coding: utf-8 -*-
import sys
import robobrowser
import re

MOBILE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Max OS X) AppleWebKit/604.5.2 (KHTML, like Gecko) Version/11.0 Mobile/15D5046b Safari/604.1"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"


class AccessToken:
    def __init__(self, email, password):
        self.access_token = self.logic(email, password)

    def logic(self, email, password):
        s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
        s.open(FB_AUTH)
        ##submit login form##
        f = s.get_form()
        f["pass"] = password
        f["email"] = email
        s.submit_form(f)
        ##click the 'ok' button on the dialog informing you that you have already authenticated with the Tinder app##
        f = s.get_form()
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        ##get access token from the html response##
        access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
        return access_token


if __name__ == '__main__':
    email, password = sys.argv[1:3]
    at = AccessToken(email, password)
    print(at.access_token)
