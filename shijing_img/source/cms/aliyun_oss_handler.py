__author__ = 'wenju'

from oss import oss_api
import service_config
import time
import config_private
# the part has been moved due to security reasons.

config = service_config.config


def upload_file_to_oss(target_path, local_file_path):
    oss = oss_api.OssAPI(config_private.private_config.oss_oss_host,
                         config_private.private_config.oss_appid,
                         config_private.private_config.oss_appkey)
    fmt = "%a, %d %b %Y %H:%M%S GMT"
    gmt_string = time.strftime(fmt, time.gmtime(time.time() + config.img_ttl))
    header = {'Expires': gmt_string}
    oss_resp = oss.put_object_from_file(config_private.private_config.oss_bucket_name,
                                        target_path, local_file_path, content_type='image/jpeg', headers=header)
    if oss_resp.status != 200:
        raise Exception(oss_resp.read())


def delete_from_oss(object_path):
    oss = oss_api.OssAPI(config_private.private_config.oss_oss_host,
                         config_private.private_config.oss_appid,
                         config_private.private_config.oss_appkey)
    oss_resp = oss.delete_object(config_private.private_config.oss_bucket_name, object_path)
    if oss_resp.status != 204:
        raise Exception(oss_resp.read())
