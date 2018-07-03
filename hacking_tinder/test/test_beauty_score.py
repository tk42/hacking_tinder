# -*- coding: utf-8 -*-
import sys
import unittest
from hacking_tinder.main.beauty_score import BeautyScore

bs = None


class TestBeautyScore(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bs = bs

    def test_KateBeckinsale(self):
        url = "https://cdn1.thr.com/sites/default/files/imagecache/landscape_928x523/2016/11/kate_beckinsale_getty_h_2016.jpg"
        result = self.bs.detect(url)
        self.assertEqual(73.148, result["score"])
        self.assertEqual("White", result["ethnicity"])

    def test_multi_faces(self):
        url = "http://images.gotinder.com/58b172266c7a43304d5b471c/1080x1080_b806b249-4fe4-44a4-8bbd-398ea26efc87.jpg"
        result = self.bs.detect(url)
        self.assertEqual(63.921, result["score"])
        self.assertEqual("Asian", result["ethnicity"])

    def test_fail_not_human(self):
        url = "http://images.gotinder.com/58b172266c7a43304d5b471c/53dc0555-fe7d-4063-81bc-50d2da792e65.jpg"
        result = self.bs.detect(url)
        self.assertEqual({"ethnicity": None, "score": 0, "url": None}, result)

    def test_fail_behind(self):
        url = "http://images.gotinder.com/59959b5403af1ed72d299cc6/1080x1080_54ac66d6-c983-464d-8ceb-b50a840dc507.jpg"
        result = self.bs.detect(url)
        self.assertEqual({"ethnicity": None, "score": 0, "url": None}, result)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        facepp_api_key = sys.argv[1]
        facepp_api_secretkey = sys.argv[2]
        sys.argv = [sys.argv[0]]
    else:
        raise ValueError("Both FACEPP_API_KEY and FACEPP_API_SECRETKEY should be specified.")
    bs = BeautyScore(facepp_api_key, facepp_api_secretkey)
    unittest.main()
