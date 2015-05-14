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
        self.img_store = configparser.get("web", "img_store")
        self.img_save_path = configparser.get("web", "img_save_path")
        self.img_size_limit = configparser.get("web", "img_size_limit")
        self.img_small_width = configparser.get("web", "img_small_width")
        self.img_small_height = configparser.get("web", "img_small_height")
        self.img_url = configparser.get("web", "img_url")

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