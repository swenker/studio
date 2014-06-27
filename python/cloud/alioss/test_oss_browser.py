__author__ = 'samsung'

import unittest
import base64
import sha
import hmac


import oss_browser



class TestOSSService(unittest.TestCase):

    @unittest.skip("this get passed")
    def test_list_buckets(self):
        oss = oss_browser.OSSService()
        oss.list_buckets()

    #@unittest.skip("")
    def test_list_service(self):
        oss = oss_browser.OSSService()
        oss.list_objects()

    @unittest.skip("")
    def test_gen_signature(self):
        oss = oss_browser.OSSService()
        print oss.gen_signature("OtxrzxIsfpFjA7SwPzILwy8Bw21TLhquhboDYROV",
                                 "PUT","c8fdb181845a4ca6b8fec737b3581d76","text/html","Thu, 17 Nov 2005 18:49:58 GMT","x-oss-magic:abracadabra\nx-oss-meta-author:foo@bar.com\n","/oss-example/nelson")

    @unittest.skip("")
    def test_gen_signature2(self):
        h=hmac.new("OtxrzxIsfpFjA7SwPzILwy8Bw21TLhquhboDYROV",
                 "PUT\nc8fdb181845a4ca6b8fec737b3581d76\ntext/html\nThu, 17 Nov 2005 18:49:58 GMT\nx-oss-magic:abracadabra\nx-oss-meta-author:foo@bar.com\n/oss-example/nelson", sha)
        print "|"+base64.encodestring(h.digest()).strip()+"|"


if __name__=="__main__":
    unittest.main()