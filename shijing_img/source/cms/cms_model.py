__author__ = 'samsung'

import json
from decimal import Decimal
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class ArticleMeta:
    def __init__(self):
        self.id = -1
        self.title = ''
        self.subtitle = ''
        self.cover = ''
        self.author = ''
        self.source = ''
        self.dtpub = ''
        self.dtupdate = ''
        self.dtcreate = ''
        self.brief = ''
        self.status = 1
        self.cid=-1
    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class ArticleEntity:
    def __init__(self,article_meta,article_content):
        self.article_meta = article_meta
        self.article_content = article_content

    def __str__(self):
        return "meta:"+self.article_meta.__str__() +"  content:"+self.article_content.__str__()

    def jsonable(self):
        return self.__dict__


class ArticleContent:
    def __init__(self,content):
        self.id = -1
        self.content = content

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__



class Comment:
    def __init__(self):
        self.title = ''
        self.content = ''
        self.ctime = None

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,"jsonable"):
            return obj.jsonable()
        elif isinstance(obj,datetime):
            return obj.strftime(TIME_FORMAT)
        elif isinstance(obj,Decimal):
            return str(obj)
        else:
            raise TypeError,"Object of type %s with value of %s is not JSON serializable" %(type(obj),repr(obj))





