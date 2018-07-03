# -*- coding: utf-8 -*-
import sys
import json
import requests
import hashlib

API_URL = 'https://api-us.faceplusplus.com/facepp/v3/detect'
"""
Detect Docs: https://console.faceplusplus.com/documents/5679127
Analyze Docs: https://console.faceplusplus.com/documents/6329465
"""


class BeautyScore:
    def __init__(self, facepp_api_key, facepp_api_secretkey):
        self.facepp_api_key = facepp_api_key
        self.facepp_api_secretkey = facepp_api_secretkey

    def create_data(self, image_url=None):
        data = dict()
        data.update({"api_key": self.facepp_api_key})
        data.update({"api_secret": self.facepp_api_secretkey})
        hash_tokens = hashlib.sha384(image_url.encode('ascii')).hexdigest()
        data.update({"face_tokens": hash_tokens})
        data.update({"image_url": image_url})
        data.update({"return_attributes": "ethnicity,beauty"})
        return data

    def detect(self, image_url):
        try:
            res = requests.post(
                API_URL, data=self.create_data(image_url=image_url)
            )
            content = json.loads(res.content.decode('utf-8').replace("'", "\""))
            try:
                attributes = content["faces"][0]["attributes"]
                return {"ethnicity": attributes["ethnicity"]["value"],
                        "score": attributes["beauty"]["female_score"],
                        "url": image_url}
            except (KeyError, IndexError) as e:
                print(content) # debug
                return {"ethnicity": None, "score": 0, "url": None}

        except requests.HTTPError as e:
            print(str(e))
            return {"ethnicity": None, "score": 0, "url": None}


if __name__ == '__main__':
    facepp_api_key, facepp_api_secretkey = sys.argv[1:3]
    bs = BeautyScore(facepp_api_key, facepp_api_secretkey)
    # sandbox
    url ="http://images.gotinder.com/59959b5403af1ed72d299cc6/1080x1080_54ac66d6-c983-464d-8ceb-b50a840dc507.jpg"
    result = bs.detect(url)
    print(result)
