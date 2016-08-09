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
        self.code = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class Image:
    IMG_TYPE_COMMON=1
    IMG_TYPE_HOME_BANNER=2
    IMG_TYPE_HOME_GALLERY=3
    IMG_TYPE_USER=4

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
        self.ext_status=1
        self.code = None

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
    ORDER_SELECTING=1
    ORDER_SELECTED=3
    ORDER_DELIVERING=5
    ORDER_COMPLETED=7
    ORDER_CANCEL=9

    def __init__(self,uid):
        self.oid = 0
        self.title = ''
        self.remark = ''
        self.dtcreate = None
        self.dtupdate = None
        self.uid = uid
        self.total_limit = 120
        self.edit_limit = 30
        self.price=999.00
        self.status = 1
        self.venue = ''
        self.dttake = ''
        self.total = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class SiteUser:
    def __init__(self,uid=None,email=None, passwd = None, nickname = None, mobile=None, status=1 ):
        self.oid = uid
        self.email = email
        self.nickname = nickname
        self.passwd = passwd
        self.mobile = mobile
        self.status = status
        self.dtcreate = None
        self.up=SiteUserProfile()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class SiteUserProfile:
    def __init__(self):
        self.uid = None
        self.address = None
        self.birthday = None
        self.remark = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__


class Preorder():
    PO_STATUS_OPEN=1
    PO_STATUS_CLOSE=2

    def __init__(self,oid=None):
        self.oid = oid
        self.status = 1
        self.utitle = ''
        self.genre = 0
        self.mobile = ''
        self.bdesc = ''
        self.pdate = ''
        self.age = 0
        self.dtcreate = None
        self.uid = None
        self.pgid = 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

class Job():
    def __init__(self,name,jobtask):
        self.name = name
        self.jobdata = jobtask.to_jsonstr()
        self.status = 1  #init
        self.oid = 0


class PhotoJob():
    def __init__(self,order_id,relative_folder,album_id):
        self.album_id = album_id
        self.order_id = order_id
        self.relative_folder = relative_folder

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__dict__.__str__()

    def jsonable(self):
        return self.__dict__

    def to_jsonstr(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)




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





