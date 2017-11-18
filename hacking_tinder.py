# -*- coding:utf-8 -*-
import io
import sys
import pynder
import asyncio
from beauty_score import BeautyScore


class HackingTinder:
    headers = None
    loop = asyncio.get_event_loop()
    count = 0

    def __init__(self, facebook_auth_token, facepp_api_key, facepp_api_secretkey):
        self.beauty_score = BeautyScore(facepp_api_key, facepp_api_secretkey)

        self.session = pynder.Session(facebook_token=facebook_auth_token)
        self.session.matches() # get users you have already been matched with

        # self.session.update_location(LAT, LON)  # updates latitude and longitude for your profile
        # self.session.profile  # your profile. If you update its attributes they will be updated on Tinder.

        self.users = self.session.nearby_users()  # returns a iterable of users nearby

        self.logic()
        self.loop.run_forever()

    def logic(self):
        self.logic_impl()
        self.count += 1
        self.loop.call_later(1, self.logic)

    def logic_impl(self):
        try:
            user = self.users.__next__()
            print("#" + str(self.count) + ": ===================================")
            print("user.name : " + user.name)
            print("user.school : " + str(user.schools))
            print("user.bio : \n" + str(user.bio))
            face_score = self.face_score(user.photos)
            print("face_score : " + str(face_score))
            if user.instagram_username is not None:
                print("instagram_username : https://www.instagram.com/" + str(user.instagram_username))
            if face_score is not None:
                if ((face_score["ethnicity"] == "Asian" and face_score["score"] > 80)
                   or (face_score["ethnicity"] == "White" and face_score["score"] > 50)):
                    print("SENT LIKE TO HER")
                    user.like()
        except Exception as e:
            print("Some error was caught : " + str(e))

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


def init():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


if __name__ == '__main__':
    # init()
    facebook_auth_token, facepp_api_key, facepp_api_secretkey = sys.argv[1:4]
    print("Starting the authentification.")
    ht = HackingTinder(facebook_auth_token, facepp_api_key, facepp_api_secretkey)
