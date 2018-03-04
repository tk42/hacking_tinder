# -*- coding: utf-8 -*-
import asyncio
import io
import sys
import configparser
import pynder
from access_token import AccessToken
from beauty_score import BeautyScore


class HackingTinder:
    headers = None
    loop = asyncio.get_event_loop()
    count = 0

    def __init__(self, facebook_auth_token, beauty_score):
        # Authentification
        print("Starting the authentification.")
        self.beauty_score = beauty_score
        self.session = pynder.Session(facebook_token=facebook_auth_token)
        print("Authentification is succeeded. Access Token is %s" % facebook_auth_token)

        # Checking environments
        print("Checking LANG in environment variables.")

        print(sys.getdefaultencoding())
        print(sys.stdout.encoding)

        # Create sessions
        self.session.matches() # get users you have already been matched with
        # self.session.update_location(LAT, LON)  # updates latitude and longitude for your profile
        # self.session.profile  # your profile. If you update its attributes they will be updated on Tinder.
        self.users = self.session.nearby_users()  # returns a iterable of users nearby
        if self.users is None:
            print("Failed to fetch the list of nearby_users.")
        else:
            print("Success to fetch the list of nearby_users.")

        # Set config
        try:
            self.config = configparser.ConfigParser()
            self.config.read('./hacking_tinder/resources/config.ini')
            self.score_threshold = {ethnicity: float(self.config["SCORE_THRESHOLD"][ethnicity])
                                    for ethnicity in self.config["SCORE_THRESHOLD"]}
        except Exception as e:
            print("Failed to read config. details : %s" % str(e))
            sys.exit(1)
        print("Success to read config.")

    def start(self):
        self.logic()
        self.loop.run_forever()

    def logic(self):
        self.logic_impl()
        self.count += 1
        self.loop.call_later(1, self.logic)

    def logic_impl(self):
        try:
            user = self.users.__next__()
        except Exception as e:
            print("Failed to get the next user. details:%s" % str(e))
            return None

        try:
            print("#" + str(self.count) + ": ===================================")
            print("user.name : " + user.name)
            print("user.school : " + str(user.schools))
            print("user.bio : \n" + str(user.bio))
            face_score = self.face_score(user.photos)
            print("face_score : " + str(face_score))
            if user.instagram_username is not None:
                print("instagram_username : https://www.instagram.com/" + str(user.instagram_username))
            if face_score is not None:
                if ((face_score["ethnicity"] == "Asian" and face_score["score"] > self.score_threshold["asian"])
                   or (face_score["ethnicity"] == "White" and face_score["score"] > self.score_threshold["white"])):
                    print("SENT LIKE TO HER")
                    user.like()
        except Exception as e:
            print("Failed to get the user details : " + str(e))

    def face_score(self, photo_urls):
        result = {"ethnicity": None, "score": 0}
        updated = False
        for photo_url in photo_urls:
            tmp = self.beauty_score.detect(photo_url)
            if tmp is not None and tmp["score"] > result["score"]:
                updated = True
                result = tmp
        if updated:
            return result
        else:
            return None


def test_utf8():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


if __name__ == '__main__':
    # test_utf8()
    fb_email, fb_password = sys.argv[1:3]
    facebook_auth_token = AccessToken(fb_email, fb_password).access_token
    facepp_api_key, facepp_api_secretkey = sys.argv[3:5]
    beauty_score = BeautyScore(facepp_api_key, facepp_api_secretkey)
    ht = HackingTinder(facebook_auth_token, beauty_score)
    ht.start()
