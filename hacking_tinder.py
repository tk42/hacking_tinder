# -*- coding:utf-8 -*-
import io
import sys
import pynder
import asyncio


class HackingTinder:
    headers = None
    loop = asyncio.get_event_loop()
    count = 0

    def __init__(self, facebook_auth_token):
        self.session = pynder.Session(facebook_token=facebook_auth_token)
        self.session.matches() # get users you have already been matched with

        # self.session.update_location(LAT, LON)  # updates latitude and longitude for your profile
        # self.session.profile  # your profile. If you update its attributes they will be updated on Tinder.

        self.users = self.session.nearby_users()  # returns a iterable of users nearby

        self.logic()
        self.loop.run_forever()

    def logic(self):
        print("Sending the heartbeat.")
        self.logic_impl()
        self.count += 1
        self.loop.call_later(1, self.logic)

    def logic_impl(self):
        try:
            user = self.users.__next__()
            print("#" + str(self.count) + ": ===================================")
            print(user.name)
            print(user.bio)
            print(user.photos)
            print(user.instagram_username)
            user.like()
        except Exception as e:
            print("Some error was caught : " + str(e))


def init():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


if __name__ == '__main__':
    # init()
    facebook_auth_token = sys.argv[1]
    print("Starting the authentification.")
    ht = HackingTinder(facebook_auth_token)
