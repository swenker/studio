__author__ = 'wenju'

from oss import oss_api


bucket_name = "simage"
oss_host="oss-cn-beijing.aliyuncs.com"
appid="MKD6WfLZOSq03lKl"
appkey="brNGbHQjtKE1SQ4mDuPuPEO4nc0lJB"

def upload_file_to_oss(target_path,local_file_path):

        oss = oss_api.OssAPI(oss_host,appid,appkey)
        oss_resp = oss.put_object_from_file(bucket_name,target_path,local_file_path,'image/jpeg')

        if oss_resp.status != 200:
            raise Exception(oss_resp.read())


def delete_from_oss(object_path):

        oss = oss_api.OssAPI(oss_host,appid,appkey)
        #print object_path
        oss_resp = oss.delete_object(bucket_name,object_path)

        if oss_resp.status != 204:
            raise Exception(oss_resp.read())
