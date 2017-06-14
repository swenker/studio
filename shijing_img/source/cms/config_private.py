__author__ = 'wenjusun'

from ConfigParser import ConfigParser

class PrivateConfig():
    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read('/var/shijing/conf/private.cfg')

        self.oss_bucket_name = config_parser.get('oss','bucket_name')
        self.oss_oss_host = config_parser.get('oss','oss_host')
        self.oss_appid = config_parser.get('oss','appid')
        self.oss_appkey = config_parser.get('oss','appkey')

        self.db_dbn = config_parser.get('db', 'dbn', 'mysql')
        self.db_host = config_parser.get('db', 'host', 'localhost')
        self.db_db = config_parser.get('db', 'db')
        self.db_user = config_parser.get('db', 'user')
        self.db_user_passwd = config_parser.get('db','passwd')


private_config = PrivateConfig()
