__author__ = 'wenju'

import decimal
import web
import os

from backend_service_helper import *
from cms_model import *
from aliyun_oss_handler import *
import cms_utils


TABLE_ARTICLE_META = "cms_article_meta"
TABLE_ARTICLE_CONTENT = "cms_article_content"

TABLE_CATEGORY = "cms_category"
TABLE_ARTICLE_CATEGORY = "cms_article_category"

TABLE_ALBUM = "cms_album"
TABLE_ALBUM_IMG = "cms_album_img"

TABLE_SITE_USER = 'site_user'
TABLE_SITE_USER_PROFILE = 'site_user_profile'

TABLE_SITE_ORDER = 'site_order'
TABLE_ORDER_IMG = 'site_order_img'

TABLE_PREORDER = 'site_preorder'

decimal.getcontext().prec = 2
config = service_config.config
logger = config.getlogger()

#web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd, charset="UTF-8")
db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=cms_utils.decrypt(config.passwd,config.passwd_padding))
db.printing=config.web_debug

album_map = {}
category_map = {}


class CmsService:
    def __init__(self):
        logger.info("===============CmsService start initialized ===============")

        album_list = self.get_album_list()
        for album in album_list:
            album_map[album.code] = album

        category_list = self.get_category_list()
        for category in category_list:
            category_map[category.code] = category

        logger.info(album_map)
        logger.info(category_map)
        logger.info("===============CmsService initialized successfully===============")

    def get_last_id(self,db):
        result = db.query("select LAST_INSERT_ID() AS mid ")
        mid = -1
        if result:
            mid = result[0]['mid']
        return mid

    def new_article(self, article):
        if article and article.article_meta.oid > 0:
            logger.error("should go to update with id:" % article.oid)
            return

        article_meta = article.article_meta

        t = db.transaction()
        try:
            sqls = "INSERT INTO %s(content)VALUES($content) " % TABLE_ARTICLE_CONTENT

            db.query(sqls, vars={'content': article.article_content.content})

            result = db.query("select LAST_INSERT_ID() AS mid ")
            cid = -1
            if result:
                cid = result[0]['mid']

            time_now = get_timenow()
            sqls = "INSERT INTO %s(title,subtitle,author,source,dtpub,dtcreate,dtupdate,cover,brief,cid,ctid) VALUES" \
                   "($title,$subtitle,$author,$source,$dtpub,$dtcreate,$dtupdate,$cover,$brief,$cid,$ctid)" \
                   % TABLE_ARTICLE_META

            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtpub': article_meta.dtpub, 'dtcreate': time_now, 'dtupdate': time_now,
                           'cover': article_meta.cover, 'brief': article_meta.brief, 'cid': cid,
                           "ctid": article_meta.ctid}
            )

            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            t.commit()

            # TODO one to many
            #sqls = "INSERT INTO %s(aid,ctid)VALUES($aid,ctid) " % (TABLE_ARTICLE_CATEGORY,mid,ctid)

            logger.info("articleId [%d] is created" % mid)
            return mid

        except Exception, e:
            logger.exception(e)
            t.rollback()
            return -1

    def update_article(self, article):
        article_meta = article.article_meta

        t = db.transaction()
        try:
            sqls = "UPDATE %s SET content=$content WHERE id=$oid " % TABLE_ARTICLE_CONTENT

            db.query(sqls,
                     vars={'content': article.article_content.content, 'oid': article.article_content.oid}
            )

            sqls = "UPDATE %s SET title=$title,subtitle=$subtitle,author=$author,source=$source,dtupdate=$dtupdate,dtpub=$dtpub,cover=$cover,brief=$brief,ctid=$ctid WHERE id=$oid" \
                   % TABLE_ARTICLE_META

            # logger.debug(sqls)
            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtpub' :article_meta.dtpub,
                           'dtupdate': get_timenow(), 'cover': article_meta.cover, 'brief': article_meta.brief,
                           'ctid': article_meta.ctid,
                           'oid': article_meta.oid}
            )

            t.commit()

            logger.info("articleId [%d] is updated" % article_meta.oid)

        except Exception, e:
            logger.exception("failed to update article with id=%d" % article_meta.oid, exc_info=e)
            t.rollback()


    #TODO delete related images
    def delete_article(self, oid, hard=False):

        if not hard:

            sqls = "UPDATE %s SET `status`=%d where id=$oid" % (TABLE_ARTICLE_META, 2)

        else:

            sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'oid': oid})
        logger.info("articleId [%d] is deleted" % oid)

    def disable_article(self, oid):

        sqls = "UPDATE %s SET `status`=$status where id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'status': 0, 'oid': oid})

        logger.info("articleId [%d] is disabled" % oid)


    def enable_article(self, oid):

        sqls = "UPDATE %s SET `status`=$status where id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'status': 1, 'oid': oid})

        logger.info("articleId [%d] is enabled" % oid)


    def list_articles(self, start, nfetch, ctcode=None, query_in_title=None, status=None):
        """list articles meta without content  """
        sql_total = "SELECT COUNT(*) as total FROM cms_article_meta "

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status,ctid FROM %s " % (
            TABLE_ARTICLE_META)

        has_condition = False
        if ctcode or query_in_title or status:
            sqls += " WHERE "
            sql_total += " WHERE "

        if ctcode:
            ctid = category_map[ctcode].oid
            has_condition = True
            sqls += " ctid=" + str(ctid)
            sql_total += " ctid=" + str(ctid)

        if query_in_title:
            if has_condition:
                sqls += " AND "
                sql_total += " AND "
            else:
                has_condition = True

            sqlwhere = " title LIKE '%s' OR brief LIKE '%s" % (query_in_title, query_in_title)

            sqls += sqlwhere
            sql_total += sqlwhere

        if status:
            if has_condition:
                sqls += " AND "
                sql_total += " AND "

            sqls += " status=" + status
            sql_total += " status=" + status

        sqls += " ORDER BY dtpub desc,dtcreate desc "

        sqls += " LIMIT $start,$nfetch"

        total = 0

        result = db.query(sql_total)

        if result:
            total = result[0]['total']

        # logger.debug(sqls)
        if query_in_title:
            result = db.query(sqls, vars={'keywords': query_in_title, 'start': start, 'nfetch': nfetch})

        else:
            result = db.query(sqls, vars={'start': start, 'nfetch': nfetch})

        rlist = []

        if result:
            for r in result:
                article_meta = self.compose_article_meta(r)
                #print article_meta
                rlist.append(article_meta)

        return rlist, total

    def search_articles(self, start, nfetch,kw=None):
        """list articles meta without content  """
        sql_total = "SELECT COUNT(*) as total FROM cms_article_meta "

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status,ctid FROM %s WHERE status=1" % (
            TABLE_ARTICLE_META)

        has_condition = False

        if kw:
            sqls += " AND "
            sql_total += " AND "

            sqlwhere = " title LIKE '%s' OR brief LIKE '%s" % (kw, kw)

            sqls += sqlwhere
            sql_total += sqlwhere

        sqls += " ORDER BY dtpub desc,dtcreate desc "

        sqls += " LIMIT $start,$nfetch"

        total = 0

        result = db.query(sql_total)

        if result:
            total = result[0]['total']

        if kw:
            result = db.query(sqls, vars={'keywords': kw, 'start': start, 'nfetch': nfetch})

        else:
            result = db.query(sqls, vars={'start': start, 'nfetch': nfetch})

        rlist = []

        if result:
            for r in result:
                article_meta = self.compose_article_meta(r)
                rlist.append(article_meta)

        return rlist, total


    def get_article(self, oid):
        sqls = "SELECT m.id AS id,m.title AS title,m.subtitle AS subtitle,m.author AS author,m.source AS source,m.dtpub AS dtpub," \
               "m.dtupdate AS dtupdate,m.dtcreate AS dtcreate,m.cover AS cover,m.brief AS brief,m.cid AS cid,m.status AS status,m.ctid as ctid,c.content AS content " \
               "FROM cms_article_meta m inner join cms_article_content c on m.cid=c.id where m.id=$oid"

        result = db.query(sqls, vars={'oid': oid})

        if result:
            r = result[0]
            article_meta = self.compose_article_meta(r)
            article_content = ArticleContent(r['content'])
            article_content.oid = r['cid']

            article = ArticleEntity(article_meta, article_content)

            return article

    def get_article_meta(self, oid):

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status,ctid FROM cms_article_meta where id=$oid"

        result = db.query(sqls, vars={'oid': oid})

        if result:
            r = result[0]
            article_meta = self.compose_article_meta(r)

            return article_meta


    def get_article_content(self, oid):
        sqls = "SELECT content FROM cms_article_content where id=$oid"

        result = db.query(sqls, vars={'oid': oid})
        if result:
            r = result[0]
            article_content = ArticleContent(r['content'])
            article_content.oid = oid

            return article_content


    def compose_article_meta(self, r):

        article_meta = ArticleMeta()
        article_meta.oid = r['id']
        article_meta.title = r['title']
        article_meta.subtitle = r['subtitle']
        article_meta.author = r['author']
        article_meta.source = r['source']
        article_meta.dtpub = r['dtpub']
        article_meta.dtupdate = r['dtupdate']
        article_meta.dtcreate = r['dtcreate']
        article_meta.cover = r['cover']
        article_meta.brief = r['brief']
        article_meta.cid = r['cid']
        article_meta.ctid = r['ctid']

        return article_meta

    # ------------------------------------------------------ category
    def save_category(self, category):

        if category.oid and category.oid > 0:
            self.update_category(category)

        else:
            self.create_category(category)

    def create_category(self, category):

        sqls = "INSERT INTO %s(title,code,dtcreate,remark)VALUES($title,$code,$dtcreate,$remark) " % TABLE_CATEGORY

        db.query(sqls, vars={'title': category.title, 'code': category.code, 'dtcreate': get_timenow(), 'remark': category.remark} )

        logger.info("category %s created" % category)

    def update_category(self, category):

        sqls = "UPDATE %s SET title=$title,code=$code,remark=$remark WHERE id=$oid" % TABLE_CATEGORY

        db.query(sqls, vars={'title': category.title, 'code': category.code, 'remark': category.remark, 'oid': category.oid} )

        logger.info("category %s updated" % category)

    def delete_category(self, oid, hard=False):

        if not hard:
            sqls = "UPDATE %s SET `status`=%d where id=$oid" % (TABLE_CATEGORY, 2)

        else:
            sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_CATEGORY

        db.query(sqls, vars={'oid': oid})

        logger.info("catetory [%d] is deleted" % oid)

    def get_category(self, oid):
        sqls = "SELECT * FROM %s WHERE id=$oid" % TABLE_CATEGORY
        result = db.query(sqls, vars={'oid': oid})

        if result:
            r = result[0]
            cate = self.compose_category(r)
            return cate


    def get_category_list(self):

        result = db.select(TABLE_CATEGORY, order="code")

        rlist = []

        if result:
            for r in result:
                cate = self.compose_category(r)
                rlist.append(cate)

        return rlist


    # Album
    def save_album(self, album):

        if album.oid and album.oid > 0:
            self.update_album(album)

        else:
            self.create_album(album)

    def create_album(self, album):

        sqls = "INSERT INTO %s(title,dtcreate,remark)VALUES($title,$dtcreate,$remark) " % TABLE_ALBUM

        db.query(sqls, vars={'title': album.title, 'dtcreate': get_timenow(), 'remark': album.remark} )

        logger.info("album %s created" % album)

    def update_album(self, album):

        sqls = "UPDATE %s SET title=$title,remark=$remark WHERE id=$oid" % TABLE_ALBUM

        db.query(sqls, vars={'title': album.title, 'remark': album.remark, 'oid': album.oid} )

        logger.info("album %s updated" % album)


    def create_img(self, img):

        try:
            sqls = "INSERT INTO %s(title,dtcreate,file,aid,itype)VALUES($title,$dtcreate,$file,$aid,$itype)" % TABLE_ALBUM_IMG

            db.query(sqls, vars={'title': img.title, 'dtcreate': get_timenow(), 'file': img.file, 'aid': img.aid, 'itype': img.itype} )

            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            logger.info("image [%d] is created" % mid)
            return mid

        except Exception, e:
            logger.exception("failed to create image:%s" % img, e)


    #TODO update image title by oid
    def update_img(self, oid, title):
        try:
            sqls = "UPDATE %s SET title=$title WHERE id=$oid" % TABLE_ALBUM_IMG

            db.query(sqls, vars={'title': title, 'oid': oid} )

            logger.info("image [%d] is updated with title:%s" % (oid,title) )
        except StandardError as e:
            logger.exception("failed to update img:%d" % oid, exc_info=e)


    def create_imglist(self, aid, imglist):

        t = db.transaction()

        try:
            for img in imglist:
                sqls = "INSERT INTO %s(title,dtcreate,file,aid)VALUES($title,$dtcreate,$file,$aid,$itype)" % ( TABLE_ALBUM_IMG)
                vars = {'title': img.title, 'dtcreate': get_timenow(), 'file': img.file, 'aid': aid, 'itype': img.itype}

                db.query(sqls, vars)

            t.commit()

        except StandardError as e:
            logger.error("failed to create images:%s" % e)
            t.rollback()

    def get_img(self, oid):
        sqls = "SELECT * FROM %s WHERE id=$oid" % TABLE_ALBUM_IMG
        result = db.query(sqls, vars={'oid': oid})
        if result:
            r = result[0]
            img = self.compose_image(r)

            return img

    #TODO delete related images
    def delete_album(self, oid):

        sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_ALBUM

        db.query(sqls, vars={'oid': oid})

        logger.info("album [%d] is deleted" % oid)


    def delete_img(self, oid):
        sqls = "SELECT file,itype FROM %s WHERE id=$oid" % TABLE_ALBUM_IMG
        result = db.query(sqls, vars={'oid': oid})
        img_path = None
        itype=-1
        if result:
            r = result[0]
            img_path = r['file']
            itype = r['itype']

        if img_path:
            # remove start / because oss does accept the start /
            img_path_raw = "raw" + img_path
            # self.delete_image_file(img_path_raw)

            img_path_thumb = "thumb" + img_path
            self.delete_image_file(img_path_thumb)

            img_path_mid = "mid" + img_path
            self.delete_image_file(img_path_mid)

            img_path_lar = "lar" + img_path
            self.delete_image_file(img_path_lar)


        sqls = "DELETE FROM %s WHERE id=$criteria" % TABLE_ALBUM_IMG

        db.query(sqls, vars={'criteria': oid})

        #order
        if itype == Image.IMG_TYPE_USER:
            sqls = "DELETE FROM %s WHERE iid=$criteria" % TABLE_ORDER_IMG
            db.query(sqls, vars={'criteria': oid})


        logger.info("image [%d] are deleted" % oid)

    def delete_image_file(self,img_path):
        try:
            os.remove(config.img_save_path+'/'+img_path)
            if config.img_store == 'oss':
                delete_from_oss(img_path)
            logger.debug("%s is deleted "%img_path)

        except StandardError as se:
            logger.error("Failed to remove file(%s):%s" % (img_path,str(se.args)))


    def delete_order_img(self, order_id):

        sqls = "SELECT iid FROM %s WHERE oid=$order_id" % TABLE_ORDER_IMG
        result = db.query(sqls, vars={'order_id': order_id})

        if result:
            t = db.transaction()
            for r in result:
                image_id = r['iid']
                self.delete_img(image_id)

            t.commit()


   #TODO to optimize the in style
    def delete_imglist(self, idlist):

        ialist=[]
        for iid in idlist.split(','):
            if iid:
                ialist.append(int(iid))

        criteria=tuple(ialist)

        sqls = "DELETE FROM %s WHERE id in $criteria" %( TABLE_ALBUM_IMG)

        db.query(sqls, vars={'criteria': criteria})

        logger.info("image [%s] are deleted" % idlist)


    def move_imglist_to_album(self, idlist,new_acode):

        ialist=[]
        for iid in idlist.split(','):
            if iid:
                ialist.append(int(iid))

        criteria=tuple(ialist)
        new_aid = album_map.get(new_acode).oid
        sqls = "UPDATE %s SET aid=$aid WHERE id in $criteria" % TABLE_ALBUM_IMG

        db.query(sqls, vars={'aid':new_aid,'criteria': criteria})

        logger.info("image [%s] are moved" % idlist)


    def get_album_list(self):

        result = db.select(TABLE_ALBUM, order="id")

        rlist = []

        if result:
            for r in result:
                album = self.compose_album(r)
                rlist.append(album)

        return rlist


    def get_album_imglist(self, acode, start=0, nfetch=20, itype=1):

        aid = album_map.get(acode).oid
        total = 0

        sql_total = "SELECT COUNT(*) as total FROM %s WHERE aid=$aid and itype=$itype " % TABLE_ALBUM_IMG

        total_query = db.query(sql_total, vars={'aid': aid, 'itype': itype})

        if total_query:
            total = total_query[0]['total']

        sqls = "SELECT * FROM %s WHERE aid=$aid and itype=$itype ORDER BY dtcreate DESC LIMIT $start,$nfetch " % TABLE_ALBUM_IMG

        result = db.query(sqls, vars={"aid": aid, "start": start, "nfetch": nfetch, 'itype': itype})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist, total


    def get_random_pic(self,nfetch,itype=1):

        sqls = "SELECT * FROM %s WHERE itype=$itype ORDER BY rand() LIMIT $nfetch " % TABLE_ALBUM_IMG

        result = db.query(sqls, vars={ 'itype': itype,'nfetch':nfetch})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist

    def get_album_imglist2(self,start=0, nfetch=20, itype=1):

        sqls = "SELECT * FROM %s WHERE itype=$itype ORDER BY dtcreate DESC LIMIT $start,$nfetch " % TABLE_ALBUM_IMG

        result = db.query(sqls, vars={"start": start, "nfetch": nfetch, 'itype': itype})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist


    def compose_category(self, r):
        category = Category(r['id'], r['code'], r['title'])
        category.dtcreate = r['dtcreate']
        category.remark = r['remark']
        category.status = r['status']

        return category

    def compose_album(self, r):
        album = Album(r['id'], r['title'])
        album.dtcreate = r['dtcreate']
        album.remark = r['remark']
        album.status = r['status']
        album.code = r['code']

        return album

    def compose_image(self, r, ext_status=False):
        image = Image(r['id'], r['title'], r['aid'])

        if not image.oid:
            return None

        image.dtcreate = r['dtcreate']
        image.file = r['file']
        image.raw = '/raw' + image.file

        image.thumbnail = '/thumb' + image.file
        image.large = '/lar' + image.file
        image.medium = '/mid' + image.file

        image.itype = r['itype']

        if ext_status:
            image.ext_status = r['status']

        return image

    def addComment(self):
        pass


    def deleteComment(self):
        pass

    def compose_order(self, r):
        order = Order(r['uid'])
        order.oid = r['id']
        order.title = r['title']
        order.total_limit = r['total_limit']
        order.edit_limit = r['edit_limit']
        order.price = r['price']
        order.dtcreate = r['dtcreate']
        order.dtupdate = r['dtupdate']
        order.dtcomplete = r['dtcomplete']
        order.remark = r['remark']
        order.status = r['status']
        order.venue = r['venue']
        order.dttake = r['dttake']

        return order

    def compose_siteuser(self, r):
        user = SiteUser()
        user.oid = r['id']
        user.status = r['status']
        user.passwd = r['passwd']
        user.email = r['email']
        user.nickname = r['nickname']
        user.mobile = r['mobile']

        return user

    def compose_preorder(self,r):
        preorder = Preorder(r['id'])
        preorder.status = r['status']
        preorder.mobile = r['mobile']
        preorder.age = r['age']
        preorder.genre = r['genre']
        preorder.utitle = r['utitle']
        preorder.pdate = r['pdate']
        preorder.bdesc = r['bdesc']
        preorder.dtcreate = r['dtcreate']
        preorder.pgid = r['pgid']

        return preorder


    def save_order(self,order):
        if not order:
            return
        vars = {}
        if order.oid:
            sqls = "UPDATE %s SET uid=$uid,price=$price,venue=$venue,remark=$remark,title=$title,total_limit=$total_limit," \
                   "edit_limit=$edit_limit,dttake=$dttake WHERE id=$oid" % TABLE_SITE_ORDER

            vars={'uid':order.uid,'price':order.price,'venue':order.venue,'remark':order.remark,'title':order.title,
                  'total_limit':order.total_limit,'edit_limit':order.edit_limit,'dttake':order.dttake,'oid':order.oid}

        else:
            sqls = "INSERT INTO %s(uid,price,venue,remark,title,total_limit,edit_limit,dttake)VALUES($uid,$price,$venue,$remark," \
                   "$title,$total_limit,$edit_limit,$dttake)" % TABLE_SITE_ORDER

            vars={'uid':order.uid,'price':order.price,'venue':order.venue,'remark':order.remark,'title':order.title,
                  'total_limit':order.total_limit,'edit_limit':order.edit_limit,'dttake':order.dttake}

        db.query(sqls,vars)

        if not order.oid:
            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            logger.info("order [%d] is created" % mid)

            order.oid = mid
            return mid

        logger.info("order [%d] is updated" % order.oid)

        return order.oid

    def load_order(self,oid):
        if not oid:
            return

        sqls = "SELECT * FROM %s WHERE id=$oid" % TABLE_SITE_ORDER

        result = db.query(sqls,vars = {'oid':oid})
        if result:
            order = self.compose_order(result[0])

            return order

        return None

    #TODO marked as deleted instead of remove?
    def delete_order(self,oid):
        if not oid:
            return

        sqls = "DELETE  FROM %s WHERE id=$oid" % TABLE_SITE_ORDER

        db.query(sqls,vars = {'oid':oid})

        logger.info("order [%d] is deleted" % oid)


    def list_orders(self, uid=None):
        sqls = 'SELECT * FROM %s %s ORDER BY dtcreate desc '

        where_condition = ''
        if uid:
            where_condition = 'WHERE uid=' + str(uid)
        result = db.query((sqls % (TABLE_SITE_ORDER, where_condition)))

        rlist = []

        if result:
            for r in result:
                order = self.compose_order(r)
                rlist.append(order)

        return rlist


    def list_orders_bystatus(self,status,uid=None):
        sqls = 'SELECT * FROM %s %s ORDER BY dtcreate desc '

        where_condition = 'WHERE status='+str(status)
        if uid:
            where_condition += ' AND uid=' + str(uid)
        result = db.query((sqls % (TABLE_SITE_ORDER, where_condition)))

        rlist = []

        if result:
            for r in result:
                order = self.compose_order(r)
                rlist.append(order)

        return rlist


    def add_order_img(self, iid, orderid):
        sqls = 'INSERT INTO %s(oid,iid,status)VALUES($orderid,$iid,1)' % TABLE_ORDER_IMG
        db.query(sqls, vars={'orderid': orderid, 'iid': iid})


    def list_order_imgs(self, oid, status=1):
        sqls = 'SELECT a.*,b.status FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id and a.itype=4 WHERE b.oid=$oid ORDER BY a.dtcreate desc '

        result = db.query(sqls, vars={'oid': oid})

        rlist = []
        if result:
            for r in result:
                img = self.compose_image(r, True)
                if img:
                    rlist.append(img)

        return rlist

    def list_order_imgs_pagination(self, oid, status=0,start=0,offset=50):
        total = 0
        status_condition =''
        if status:
            status_condition=" AND status="+status

        sqls_total = 'SELECT count(*) as total FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id and a.itype=4 WHERE b.oid=$oid '+status_condition

        result_total = db.query(sqls_total, vars={'oid': oid})
        if result_total:
            total = result_total[0]['total']

        sqls = 'SELECT a.*,b.status FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id and a.itype=4 WHERE b.oid=$oid '+status_condition+' ORDER BY a.dtcreate desc limit $start,$offset '


        result = db.query(sqls, vars={'oid': oid,'start':start,'offset':offset})

        rlist = []
        if result:
            for r in result:
                img = self.compose_image(r, True)
                if img:
                    rlist.append(img)

        return rlist,total

    def get_order_imgcover(self, oid):
        sqls = 'SELECT a.*,b.status FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id and a.itype=4 WHERE b.oid=$oid ORDER BY a.dtcreate desc limit 1'

        result = db.query(sqls, vars={'oid': oid})

        if result:
            for r in result:
                img = self.compose_image(r, True)
                if img:
                    return img


    #TODO
    def list_selected_imgs(self, oid):
        sqls = 'SELECT a.* FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id WHERE b.oid=$oid AND b.status=2 ORDER BY a.dtcreate desc '

        result = db.query(sqls, vars={'oid': oid})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist


    def update_user_choice(self, iid, status):
        sqls = 'UPDATE site_order_img SET status=$status where iid=$iid'

        db.query(sqls, vars={'status': status, 'iid': iid})

    def get_siteuser(self,uid):
        sqls = 'SELECT id,mobile,nickname,email,status,dtcreate FROM %s WHERE id=$uid' % TABLE_SITE_USER
        result = db.query(sqls,vars={'uid':uid})
        if result:
            user = SiteUser()
            for r in result:
                user.oid = r['id']
                user.status = r['status']
                user.email = r['email']
                user.nickname = r['nickname']
                user.mobile = r['mobile']
                user.dtcreate = r['dtcreate']

                user.up = self.get_siteuser_profile(user.oid)
            return user

    def get_siteuser_profile(self,uid):
        sqls = 'SELECT address,birthday,remark FROM %s WHERE uid=$uid' % TABLE_SITE_USER_PROFILE
        result = db.query(sqls,vars={'uid':uid})
        if result:
            sup = SiteUserProfile()
            for r in result:
                sup.uid = uid
                sup.address = r['address']
                sup.birthday = r['birthday']
                sup.remark = r['remark']

            return sup

    def save_siteuser(self,**userinfo):
        sqls = "UPDATE %s SET email=$email,nickname=$nickname,mobile=$mobile,status=$status WHERE id=$uid" % TABLE_SITE_USER
        db.query(sqls, vars=userinfo)

        self.update_siteuser_profile(**userinfo)
        # self.update_siteuser_profile(**sup)

        logger.info("user:[%s] saved" %(userinfo))

    def site_user_login(self, mobile, passwd):
        sqls = 'select * from %s where mobile=$mobile' % TABLE_SITE_USER
        result = db.query(sqls, vars={'table': TABLE_SITE_USER, 'mobile': mobile})

        if result:
            for r in result:
                user = self.compose_siteuser(r)
                if user.status == 1:
                    # logger.info("passwd=%s, %s",user.passwd,md5(passwd))
                    if user.passwd == md5(passwd):
                        user.passwd=None
                        logger.info("user [%s] logged in" %user.mobile)
                        return user, 'OK'
                    else:
                        logger.info("user [%s] tried wrong passwd" %user.mobile)
                else:
                    logger.info("user [%s] status is abnormal:%d" %(user.mobile,user.status))
                    return user.status, 'status'

        logger.warn("NotFoundUser:%s" % mobile)
        return -1, 'NotFound'

    def send_mail(self, subject, message_body):
        from_address = config.mail_from_address
        to_address = config.mail_to_address
        if config.mail_smtp_host:
            web.config.smtp_server = config.mail_smtp_host

        #['user1@example.com', 'user2@example.com']
        try:
            web.sendmail(from_address,to_address,subject,message_body)
            logger.info("Mail sent to :"+to_address)
            return True
        except StandardError as e:
            logger.error("Failed to send notification email:%s ,%s " %(subject,e))
            return False

    def create_preorder(self,preorder):
        sqls = 'INSERT INTO '+TABLE_PREORDER+'(utitle,mobile,genre,age,bdesc,pdate,pgid)values($utitle,$mobile,$genre,$age,$bdesc,$pdate,$pgid)'

        db.query(sqls,vars = {'utitle':preorder.utitle,'mobile':preorder.mobile,'genre':preorder.genre,'age':preorder.age,'bdesc':preorder.bdesc,'pdate':preorder.pdate,'pgid':preorder.pgid})

        result = db.query("select LAST_INSERT_ID() AS mid ")
        if result:
            mid = result[0]['mid']
            logger.info("preorder [%s] is created" % mid)
            preorder.oid = mid

            return mid



    def to_order(self,preorder):
        "convert a preorder to order"


    def list_preorder(self,pgid,status,pdate=None):
        sqls = 'SELECT * FROM '+TABLE_PREORDER
        vars = None
        if pgid or status:
            sqls += " WHERE "

            if pgid and status:
                sqls += " pgid=$pgid and status=$status "
                vars={'pgid':pgid,'status': status}

            elif status:
                sqls += " status=$status "
                vars={'status': status}
            else:
                sqls += " pgid=$pgid "
                vars={'pgid':pgid}

            if pdate:
                sqls += " and pdate like '"+pdate+"%' "

        elif pdate:
            sqls += " pdate like '"+pdate+"%' "

        result = db.query(sqls,vars)

        rlist = []

        if result:
            for r in result:
                preorder = self.compose_preorder(r)
                rlist.append(preorder)

        return rlist


    def delete_preorder(self,oid):
        sqls = "DELETE FROM "+TABLE_PREORDER + " WHERE id=$id"
        db.query(sqls,vars={'id':oid})
        logger.info("preorder [%d] is deleted" % oid)


    def create_siteuser(self,siteuser):

        if not siteuser:
            return None
        sqls = "INSERT INTO %s( email,passwd ,nickname,mobile,dtcreate)VALUES($email,$passwd,$nickname,$mobile,$dtcreate)" %TABLE_SITE_USER

        t = db.transaction()

        mid = -1
        try:
            db.query(sqls,vars = {'email':siteuser.email,'passwd':md5(siteuser.passwd),'nickname':siteuser.nickname,'mobile':siteuser.mobile,'dtcreate':get_timenow()})

            result = db.query("select LAST_INSERT_ID() AS mid ")
            if result:
                mid = result[0]['mid']
            logger.info("user [%s] is created" % siteuser.mobile)

            sup = siteuser.up
            sup.uid = mid
            self.create_siteuser_profile(sup)

            t.commit()
        except StandardError as error:
            logger.error("Failed to create site user :%s " % error)
            t.rollback()

        return mid

    def create_siteuser_profile(self,siteuser_profile):
        sqls = "INSERT INTO %s( uid,address,birthday,remark)VALUES($uid,$address,$birthday,$remark)" %TABLE_SITE_USER_PROFILE
        db.query(sqls,vars = {'uid':siteuser_profile.uid,'address':siteuser_profile.address,'birthday':siteuser_profile.birthday,'remark':siteuser_profile.remark})

        oid = self.get_last_id(db)
        logger.info("user profile [%s] is created" % siteuser_profile.uid)

        return oid

    def update_siteuser_profile(self,**sup_info):
        sqls = "UPDATE %s SET address=$address,birthday=$birthday,remark=$remark WHERE uid=$uid" % TABLE_SITE_USER_PROFILE
        db.query(sqls, vars=sup_info)

        # logger.info("user profile:[%s] saved" %(sup_info))

    def delete_siteuser(self,uid):
        sqls = "DELETE FROM %s WHERE id=$uid " % TABLE_SITE_USER
        t = db.transaction()
        try:

            self.delete_siteuser_profile(uid)

            db.query(sqls,vars={'uid':uid})
            logger.info("user:[%d] deleted" % uid)

            t.commit()
        except StandardError as error:
            logger.error("Failed to delete user:%d due to: %s "%(uid,error))

    def delete_siteuser_profile(self,uid):
        sqls = "DELETE FROM %s WHERE uid=$uid " % TABLE_SITE_USER_PROFILE
        db.query(sqls,vars={'uid':uid})
        logger.info("user profile:[%d] deleted" % uid)

    def update_porder_status(self,oid,uid,status):
        sqls = "UPDATE %s SET status=$status,uid=$uid WHERE id=$oid" %TABLE_PREORDER

        db.query(sqls,vars={'oid':oid,'uid':uid,'status':status})

        logger.info("preorder [%d] is updated to [%d] by user [%d]" % (oid,status,uid) )


    def list_siteuser(self,uid=None):
        user_list = []

        if uid:
            user_list.append(self.get_siteuser(uid))
            return user_list
        else:
            sqls = "SELECT * FROM %s a LEFT JOIN %s b ON a.id=b.uid ORDER BY id" %(TABLE_SITE_USER,TABLE_SITE_USER_PROFILE)

        result = db.query(sqls)

        if result:
            for r in result:
                suser = SiteUser()
                suser.oid = r['id']
                suser.mobile = r['mobile']
                suser.email = r['email']
                suser.nickname = r['nickname']
                suser.status = r['status']
                suser.dtcreate = r['dtcreate']

                sup = SiteUserProfile()
                sup.uid = r['id']
                sup.address = r['address']
                sup.birthday = r['birthday']
                sup.remark = r['remark']
                suser.up = sup
                user_list.append(suser)

            return user_list

    def update_order_status(self,oid,status):
        try:
            if not oid or oid<1:
                logger.warn("Invalid order id "+str(oid))

            sqls = "UPDATE %s SET status=$status WHERE id=$oid" % TABLE_SITE_ORDER

            db.query(sqls,vars={'oid':oid,'status':status})

            logger.info("order [%d] status updated to %d" %(oid,status))
        except StandardError as error:
            logger.error("Failed to update order [%d] status to [%d],due to :%s" %(oid,status,error))

    def get_total_siteuser(self):
        sqls = "SELECT COUNT(*) as total FROM %s " % TABLE_SITE_USER

        result = db.query(sqls)

        if result:
            return result[0]['total']

    def get_total_order(self):
        sqls = "SELECT COUNT(*) as total FROM %s " % TABLE_SITE_ORDER

        result = db.query(sqls)

        if result:
            return result[0]['total']

    def get_agenda(self,pid):
        "Return photographer's agenda"
        return []


cmsService = CmsService()



