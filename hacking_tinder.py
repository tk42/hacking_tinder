# -*- coding:utf-8 -*-
import json
import asyncio
from scapy.all import *
import requests
from munch import Munch

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
RECS_URL = "https://api.gotinder.com/recs/core?locale=ja"


class SuiffingPacket:
    loop = asyncio.get_event_loop()
    buff_size = 2048

    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        self.sniff()
        self.loop.run_forever()

    def sniff(self):
        # pkt = self.conn.recv(self.buff_size)
        # hexvalue = binascii.hexlify(pkt).decode()
        # print([hexvalue[i:i + 2] for i in range(0, len(hexvalue), 2)])
        sniff(filter="tcp and port 80", prn=self.packet_callback, store=0)
        self.loop.call_later(0.1, self.sniff)

    def packet_callback(self, packet):
        http_packet=str(packet)
        if http_packet.find('GET'):
            return self.get_print(packet)

    def get_print(self, packet1):
        ret = "*****GET PACKET*****\n"
        ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
        ret += "********************\n"
        return ret


class HackingTinder:
    headers = None
    loop = asyncio.get_event_loop()
    counter = 0

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
            like_json = requests.get(self.make_like_url(person._id), headers=self.headers)
            res = json.loads((like_json.text))
            if "status" in res and res["status"] == 401:
                raise RuntimeError(
                    "Something is wrong. It might be because make_like_url() is failed with the expire X-Auth-Token."
                )
            print("#" + str(self.counter) + ": SENT LIKE TO HER (" + person._id + ") : " + like_json.text)
            self.counter += 1
            time.sleep(0.1)

        self.loop.call_soon(self.logic)

    def get_recs(self):
        result = []
        try:
            recs_json = requests.get(RECS_URL, headers=self.headers)
            recs = Munch(json.loads(recs_json.text))
            for rec in recs.results:
                result.append(Munch(rec))
            return result
        except:
            raise RuntimeError(
                "Something is wrong. It might be because make_like_url() is failed with the expire X-Auth-Token."
            )

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
    SuiffingPacket()
    # try:
    #     token = str(sys.argv[1])
    #     ht = HackingTinder(token)
    # except IndexError:
    #     print("X-Auth-Token IS EMPTY.")