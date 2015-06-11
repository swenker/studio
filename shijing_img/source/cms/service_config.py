__author__ = 'wenju'

import logging.config
from ConfigParser import ConfigParser
import os.path


class ServiceConfig():
    # _instance =
    def __init__(self, confpath):
        conf_file = confpath + "/cms.cfg"
        # print os.path.abspath(conffile)
        if not os.path.exists(os.path.abspath(conf_file)):
            # guess it. it takes effect for test mostly
            confpath += "/local"
            print "------------------"
            print "Attention:[%s] does not exist,the following path will be used:\n[%s]" % (
                os.path.abspath(conf_file), os.path.abspath(confpath))
            print "------------------"

        logging.config.fileConfig(confpath + "/log.cfg")

        configparser = ConfigParser()
        configparser.read(confpath + "/cms.cfg")
        self.configparser = configparser

        self.dbn = configparser.get('db', 'dbn', 'mysql')
        self.host = configparser.get('db', 'host', 'localhost')
        self.db = configparser.get('db', 'db')
        self.user = configparser.get('db', 'user')
        self.passwd = configparser.get('db', 'passwd')

        self.web_base = configparser.get("web", "web_base")
        self.img_store = configparser.get("img", "store")
        self.img_save_path = configparser.get("img", "save_path")
        self.img_size_limit = int(configparser.get("img", "size_limit"))

        self.img_thumb_width = configparser.get("img", "thumb_width")
        self.img_thumb_height = configparser.get("img", "thumb_height")

        self.img_medium_width = configparser.get("img", "medium_width")
        self.img_medium_height = configparser.get("img", "medium_height")

        self.img_large_width = configparser.get("img", "large_width")
        self.img_large_height = configparser.get("img", "large_height")

        self.img_url = configparser.get("img", "url")

        self.img_watermark_text = configparser.get("img", "watermark_text")
        self.img_watermark_text_size = int(configparser.get("img", "watermark_text_size"))
        self.img_watermark_text_font = configparser.get("img", "watermark_text_font")
        self.img_watermark_angle = int(configparser.get("img", "watermark_angle"))
        self.img_watermark_opacity = float(configparser.get("img", "watermark_opacity"))

        self.img_ttl = float(configparser.get("img", "ttl"))



        self.ctcode_portfolio = configparser.get("web", "ctcode_portfolio")
        self.ctcode_service = configparser.get("web", "ctcode_service")
        self.ctcode_school = configparser.get("web", "ctcode_school")
        self.ctcode_news = configparser.get("web", "ctcode_news")
        self.ctcode_article = configparser.get("web", "ctcode_article")




    def __repr__(self):
        # TODO
        #return "dbn=%s, db=%s, host=%s, user=%s, passwd=%s" %(self.dbn,self.db,self.host,self.user,self.passwd)
        return self.__dict__.__repr__()

    def getlogger(self, loggername="cms"):
        return logging.getLogger(loggername)


config = ServiceConfig("/var/shijing/conf")

config.getlogger("ServiceConfig").info("Service Config loaded successfully..")
config.getlogger("ServiceConfig").info(config)