__author__ = 'wenju'

import json
from decimal import Decimal
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class ArticleMeta:
    def __init__(self):
        self.oid = -1
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
        self.cid = -1
        self.ctid = -1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class ArticleEntity:
    def __init__(self, article_meta, article_content):
        self.article_meta = article_meta
        self.article_content = article_content

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "meta:" + self.article_meta.__str__() + "  content:" + self.article_content.__str__()

    def jsonable(self):
        return self.__dict__


class ArticleContent:
    def __init__(self, content):
        self.oid = -1
        self.content = content

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class Category:
    def __init__(self, id=-1,code=None,title=None):
        self.code = code
        self.title = title
        self.oid = id
        self.status = 1
        self.dtcreate = None
        self.remark = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class Album:
    def __init__(self, id=-1, title=None):
        self.title = title
        self.oid = id
        self.status = 1
        self.dtcreate = None
        self.remark = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class Image:
    def __init__(self, id=-1, title=None, aid=-1, file=None):
        self.title = title
        self.oid = id
        self.aid = aid
        self.file = file

        self.thumbnail = ''
        self.medium = ''
        self.large = ''
        self.raw = ''

        #itype = 1,2,3  [1:common, 2,homepage-banner 3,homepage-gallery,4 for user]
        self.itype=1


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class Comment:
    def __init__(self):
        self.title = ''
        self.content = ''
        self.ctime = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class Order:
    def __init__(self,uid):
        self.oid = 0
        self.remark = ''
        self.dtcreate = None
        self.dtupdate = None
        self.dtcomplete = None
        self.uid = uid
        self.price=None
        self.status = 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class SiteUser:
    def __init__(self,uid,email, passwd, nickname = None, mobile=None, status=1 ):
        self.oid = 0
        self.uid = uid
        self.email = email
        self.nickname = nickname
        self.passwd = passwd
        self.mobile = mobile
        self.status = status


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__




class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "jsonable"):
            return obj.jsonable()
        elif isinstance(obj, datetime):
            return obj.strftime(TIME_FORMAT)
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            raise TypeError, "Object of type %s with value of %s is not JSON serializable" % (type(obj), repr(obj))





