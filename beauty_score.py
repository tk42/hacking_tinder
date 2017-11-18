# -*- coding: utf-8 -*-
import sys
import json
import requests
import hashlib

HTTP_URL = 'https://api-us.faceplusplus.com/facepp/v3/detect'
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
                        HTTP_URL,
                        data=self.create_data(image_url=image_url)
            )
            content = json.loads(res.content.decode('utf-8').replace("'", "\""))
            try:
                attributes = content["faces"][0]["attributes"]
                return {"ethnicity": attributes["ethnicity"]["value"],
                        "score": attributes["beauty"]["female_score"],
                        "url": image_url}
            except IndexError as e:
                return None

        except requests.HTTPError as e:
            print(str(e))


if __name__ == '__main__':
    facepp_api_key, facepp_api_secretkey = sys.argv[1:3]
    bs = BeautyScore(facepp_api_key, facepp_api_secretkey)
    # result = bs.detect("http://images.gotinder.com/596ebcaf36a7be556daf9cc3/1080x1080_3e803adb-d975-4957-8ca7-fc78c7cc145d.jpg")
    # result = bs.detect("http://images.gotinder.com/55e19e96aee02d7b47761eb8/1080x1080_d518ea5b-f086-46b7-8dac-f44dab682232.jpg")
    # result = bs.detect("http://images.gotinder.com/58b172266c7a43304d5b471c/53dc0555-fe7d-4063-81bc-50d2da792e65.jpg")
    # result = bs.detect("http://images.gotinder.com/58b172266c7a43304d5b471c/1080x1080_b806b249-4fe4-44a4-8bbd-398ea26efc87.jpg")
    result = bs.detect("http://images.gotinder.com/59959b5403af1ed72d299cc6/1080x1080_54ac66d6-c983-464d-8ceb-b50a840dc507.jpg")
    print(result)
