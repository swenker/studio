__author__ = 'samsung'


import httplib
import base64
import hmac
import time
import hashlib
import urllib


#http://oss-example.oss-cn-hangzhou.aliyuncs.com/oss-api.pdf?OSSAccessKeyId=44CF9590006BF252F707&Expires=1141889120&Signature=vjbyPxybdZaNmGa%2ByT272YEAiv4%3D

access_id="nhkyOTAlyeaBbPvm"
access_key="gfAlfeb8ZhxaklYILwHpA5I1zvc5J8"

class OSSService():
    def __init__(self,oss_host='oss-cn-hangzhou.aliyuncs.com',bucket=None):
        self.oss_host = oss_host
        self.bucket = bucket


    def list_buckets(self,path='/'):
        #passed
        conn = httplib.HTTPConnection(self.oss_host)
        params = urllib.urlencode({"max-keys":"2"})

        headers={}

        gmt_time=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        headers["Date"]=gmt_time

        signature = self.gen_signature(access_key,"GET","","",gmt_time,"",path)

        authorization = "OSS %s:%s" % (access_id,signature)

        headers["Authorization"]=authorization
        headers["Host"]="oss-cn-hangzhou.aliyuncs.com"

        conn.request("GET",path,params,headers)
        resp = conn.getresponse()

        print resp.status,resp.reason

        data = resp.read()

        print data

        conn.close()

    def list_objects(self,path='/smagazine-st'):
        conn = httplib.HTTPConnection(self.oss_host)
        params = urllib.urlencode({"prefix":"pic","delimiter":"/"})
        params = None

        headers={}

        gmt_time=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        headers["Date"]=gmt_time

        signature = self.gen_signature(access_key,"GET","","",gmt_time,"",path)

        authorization = "OSS %s:%s" % (access_id,signature)

        headers["Authorization"]=authorization
        headers["Host"]="oss-cn-hangzhou.aliyuncs.com"

        conn.request("GET",path,params,headers)
        resp = conn.getresponse()

        print resp.status,resp.reason

        data = resp.read()

        print data

        conn.close()


    def gen_signature(self,skey,method,content_md5,content_type,date,canonicalized_oss_headers="",canonicalized_resource=""):
        string_to_sign = method + "\n" + content_md5.strip() + "\n" + content_type + "\n" + date + "\n" + canonicalized_oss_headers + canonicalized_resource
        h = hmac.new(skey,string_to_sign,hashlib.sha1)
        return base64.encodestring(h.digest()).strip()


def convert_utf8(input_string):
    if isinstance(input_string, unicode):
        input_string = input_string.encode('utf-8')
    return input_string



