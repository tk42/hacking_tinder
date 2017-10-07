# -*- coding:utf-8 -*-
import sys
import time
import json
import asyncio
import requests
from munch import Munch

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
RECS_URL = "https://api.gotinder.com/recs/core?locale=ja"


class HackingTinder():
    headers = None
    loop = asyncio.get_event_loop()

    def __init__(self, token):
        self.headers = {
            "User-Agent": USER_AGENT,
            "X-Auth-Token": token
        }
        self.logic()
        self.loop.run_forever()

    def logic(self):
        persons = self.get_recs()

        for person in persons:
            # self.print_person_info(person)
            id = person._id
            like_json = requests.get(self.make_like_url(id), headers=self.headers)
            print("SENT LIKE TO HER (" + id + ") : " + like_json.text)
            time.sleep(0.1)

        self.loop.call_soon(self.logic)

    def get_recs(self):
        result = []
        recs_json = requests.get(RECS_URL, headers=self.headers)
        recs = Munch(json.loads(recs_json.text))
        for rec in recs.results:
            result.append(Munch(rec))
        return result

    def print_person_info(self, person):
        """
        :param person: Munch
        :return: void
        """
        try:
            print(person)
        except:
            pass
        name = person.name
        sys.stdout.buffer.write("name:" + name)

        bio = person.bio.encode('utf_8')
        sys.stdout.buffer.write("bio:" + bio)

        birth_date = person.birth_date
        sys.stdout.write("birth_date:" + birth_date)

        distance_mi = str(person.distance_mi)
        sys.stdout.write("distance_mi:" + str(distance_mi))

        photos = person.photos
        sys.stdout.write("photos:" + photos)

    def make_like_url(self, id):
        return "https://api.gotinder.com/like/" + id + "?locale=ja"

if __name__ == '__main__':
    try:
        token = str(sys.argv[1])
        ht = HackingTinder(token)
    except IndexError:
        print("X-Auth-Token IS EMPTY.")
