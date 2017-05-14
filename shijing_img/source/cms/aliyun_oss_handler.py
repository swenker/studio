__author__ = 'wenju'

from oss import oss_api
import service_config
import time

#the part has been moved due to security reasons.

config = service_config.config

def upload_file_to_oss(target_path,local_file_path):
        oss = oss_api.OssAPI(oss_host,appid,appkey)
        fmt = "%a, %d %b %Y %H:%M%S GMT"
        gmt_string = time.strftime(fmt,time.gmtime(time.time()+config.img_ttl))
        header={'Expires': gmt_string}
        oss_resp = oss.put_object_from_file(bucket_name,target_path,local_file_path, content_type='image/jpeg',headers=header)
        if oss_resp.status != 200:
            raise Exception(oss_resp.read())

def delete_from_oss(object_path):

        oss = oss_api.OssAPI(oss_host,appid,appkey)
        oss_resp = oss.delete_object(bucket_name,object_path)
        if oss_resp.status != 204:
            raise Exception(oss_resp.read())
