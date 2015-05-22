
__author__ = 'wenju'

import decimal
import web

from backend_service_helper import get_timenow
from cms_model import *
from aliyun_oss_handler import *


TABLE_ARTICLE_META = "cms_article_meta"
TABLE_ARTICLE_CONTENT = "cms_article_content"

TABLE_CATEGORY = "cms_category"
TABLE_ARTICLE_CATEGORY = "cms_article_category"

TABLE_ALBUM = "cms_album"
TABLE_ALBUM_IMG = "cms_album_img"


TABLE_SITE_USER='site_user'
TABLE_SITE_ORDER='site_order'
TABLE_ORDER_IMG='site_order_img'

decimal.getcontext().prec=2
config = service_config.config
logger = config.getlogger("CmsService")

# db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd, charset="UTF-8")
db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd)


class CmsService:
    def __init__(self):
        pass

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
            sqls = "INSERT INTO %s(title,subtitle,author,source,dtpub,dtcreate,dtupdate,cover,brief,cid,ctcode) VALUES" \
                   "($title,$subtitle,$author,$source,$dtpub,$dtcreate,$dtupdate,$cover,$brief,$cid,$ctcode)" \
                   % TABLE_ARTICLE_META

            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtpub': article_meta.dtpub, 'dtcreate': time_now, 'dtupdate': time_now,
                           'cover': article_meta.cover, 'brief': article_meta.brief, 'cid': cid,"ctcode":article_meta.ctcode}
            )

            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            t.commit()

            #TODO one to many
            #sqls = "INSERT INTO %s(aid,ctcode)VALUES($aid,ctcode) " % (TABLE_ARTICLE_CATEGORY,mid,ctcode)

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

            sqls = "UPDATE %s SET title=$title,subtitle=$subtitle,author=$author,source=$source,dtupdate=$dtupdate,cover=$cover,brief=$brief,ctcode=$ctcode WHERE id=$oid" \
                   % TABLE_ARTICLE_META

            # logger.debug(sqls)
            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtupdate': get_timenow(), 'cover': article_meta.cover, 'brief': article_meta.brief,
                           'ctcode':article_meta.ctcode,
                           'oid': article_meta.oid}
            )

            t.commit()

            logger.info("articleId [%d] is updated" % article_meta.oid)

        except Exception, e:
            logger.exception("failed to update article with id=%d" % article_meta.oid, exc_info=e)
            t.rollback()


    def delete_article(self, oid, hard=False):

        if not hard:

            sqls = "UPDATE %s SET `status`=%d where id=$oid" % (TABLE_ARTICLE_META, 2)

        else:

            sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'oid': oid})


    def disable_article(self, oid):

        sqls = "UPDATE %s SET `status`=$status where id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'status': 0, 'oid': oid})


    def enable_article(self, oid):

        sqls = "UPDATE %s SET `status`=$status where id=$oid" % TABLE_ARTICLE_META

        db.query(sqls, vars={'status': 1, 'oid': oid})


    def list_articles(self, start, nfetch, ctcode=None,query_in_title=None,status=None):
        """list articles meta without content  """
        sql_total = "SELECT COUNT(*) as total FROM cms_article_meta "

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status,ctcode FROM %s " % (TABLE_ARTICLE_META)

        has_condition = True
        if ctcode or query_in_title or status:
            sqls += " WHERE "
            sql_total += " WHERE "

        if ctcode:
            has_condition = True
            sqls += " ctcode='"+ctcode+"'"
            sql_total += " ctcode='"+ctcode+"'"

        if query_in_title:
            if has_condition:
                sqls +=" AND "
                sql_total += " AND "
            else:
                has_condition = True

            sqlwhere = " title LIKE '%s' OR brief LIKE '%s" % (query_in_title,query_in_title)

            sqls += sqlwhere
            sql_total += sqlwhere


        if status:
            if has_condition:
                sqls +=" AND "
                sql_total += " AND "

            sqls += " status="+status
            sql_total += " status="+status


        sqls += " ORDER BY dtcreate desc "

        sqls += " LIMIT $start,$nfetch"

        total = 0

        result = db.query(sql_total)

        if result:
            total = result[0]['total']

        #logger.debug(sqls)
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


    def get_article(self, oid):
        sqls = "SELECT m.id AS id,m.title AS title,m.subtitle AS subtitle,m.author AS author,m.source AS source,m.dtpub AS dtpub," \
               "m.dtupdate AS dtupdate,m.dtcreate AS dtcreate,m.cover AS cover,m.brief AS brief,m.cid AS cid,m.status AS status,m.ctcode as ctcode,c.content AS content " \
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

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status,ctcode FROM cms_article_meta where id=$oid"

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
        article_meta.ctcode = r['ctcode']

        return article_meta

    #------------------------------------------------------ category
    def save_category(self, category):

        if category.oid and category.oid > 0:

            self.update_category(category)

        else:

            self.create_category(category)

    def create_category(self, category):

        sqls = "INSERT INTO %s(title,code,dtcreate,remark)VALUES($title,$code,$dtcreate,$remark) " % TABLE_CATEGORY

        db.query(sqls,
                 vars={'title': category.title,'code': category.code, 'dtcreate': get_timenow(), 'remark': category.remark}
        )

        logger.info("category %s created" % category)

    def update_category(self, category):

        sqls = "UPDATE %s SET title=$title,code=$code,remark=$remark WHERE id=$oid" % TABLE_CATEGORY

        db.query(sqls,
                 vars={'title': category.title, 'code': category.code, 'remark': category.remark, 'oid': category.oid}
        )

        logger.info("category %s updated" % category)

    def delete_category(self, oid, hard=False):

        if not hard:

            sqls = "UPDATE %s SET `status`=%d where id=$oid" % (TABLE_CATEGORY, 2)

        else:

            sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_CATEGORY

        db.query(sqls, vars={'oid': oid})

    def get_category(self, oid):
        sqls = "SELECT * FROM %s WHERE id=$oid" % TABLE_CATEGORY
        result = db.query(sqls,vars={'oid':oid})
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

        db.query(sqls,
                 vars={'title': album.title, 'dtcreate': get_timenow(), 'remark': album.remark}
        )

        logger.info("album %s created" % album)

    def update_album(self, album):

        sqls = "UPDATE %s SET title=$title,remark=$remark WHERE id=$oid" % TABLE_ALBUM

        db.query(sqls,
                 vars={'title': album.title, 'remark': album.remark, 'oid': album.oid}
        )

        logger.info("album %s updated" % album)


    def create_img(self, img):

        try:
            sqls = "INSERT INTO %s(title,dtcreate,file,aid,itype)VALUES($title,$dtcreate,$file,$aid,$itype)" % TABLE_ALBUM_IMG

            db.query(sqls,
                     vars={'title': img.title, 'dtcreate': get_timenow(), 'file': img.file, 'aid': img.aid,'itype':img.itype}
            )

        except Exception, e:
            logger.exception("failed to create image:%s" % img, exc_info=e)


    #TODO update image title by oid
    def update_img(self, oid, title):
        try:
            sqls = "UPDATE %s SET title=$title WHERE id=$oid" % TABLE_ALBUM_IMG

            db.query(sqls,
                     vars={'title': title, 'oid': oid}
            )
        except Exception, e:
            logger.exception("failed to update img:%d" % oid, exc_info=e)


    # def create_imglist(self,imglist):
    #
    #     t = db.transaction()
    #
    #     try:
    #         for img in imglist:
    #
    #             sqls = "INSERT INTO %s(title,dtcreate,file,aid)VALUES('%s','%s','%s',%d)" %(TABLE_ALBUM_IMG,img.title,get_timenow(),img.file,img.aid)
    #
    #             db.query(sqls)
    #
    #         t.commit()
    #
    #     except Exception, e:
    #         logger.error("failed to create images:%s" % e)
    #         t.rollback()

    def get_img(self,oid):
        sqls = "SELECT * FROM %s WHERE id=$oid" % TABLE_ALBUM_IMG
        result = db.query(sqls,vars={'oid':oid})
        if result:
            r = result[0]
            img = self.compose_image(r)
            return img


    def delete_album(self, oid):

        sqls = "DELETE FROM %s WHERE id=$oid" % TABLE_ALBUM

        db.query(sqls, vars={'oid': oid})

        logger.info("album %d is deleted" % oid)


    def delete_img(self, oid):
        sqls = "SELECT file FROM %s WHERE id=$oid" % TABLE_ALBUM_IMG
        result = db.query(sqls,vars={'oid':oid})
        img_path=None
        if result:
            r = result[0]
            img_path = r['file']
        if img_path:
            # remove start / because oss does accept the start /
            img_path = "raw"+img_path

        delete_from_oss(img_path)

        sqls = "DELETE FROM %s WHERE id=$criteria" % TABLE_ALBUM_IMG

        db.query(sqls, vars={'criteria': oid})

        logger.info("img %s are deleted" % oid)

    def delete_imglist(self, idlist):

        #criteria = ",".join(idlist)
        criteria = idlist

        sqls = "DELETE FROM %s WHERE id in ($criteria)" % TABLE_ALBUM_IMG

        db.query(sqls, vars={'criteria': criteria})

        logger.info("img %s are deleted" % criteria)


    def get_album_list(self):

        result = db.select(TABLE_ALBUM, order="title")

        rlist = []

        if result:
            for r in result:
                album = self.compose_album(r)
                rlist.append(album)

        return rlist


    def get_album_imglist(self, aid, start=0, nfetch=20,itype=1):
        total = 0

        sql_total = "SELECT COUNT(*) as total FROM %s WHERE aid=$aid and itype=$itype " % TABLE_ALBUM_IMG

        total_query = db.query(sql_total, vars={'aid': aid,'itype':itype})

        if total_query:
            total = total_query[0]['total']

        sqls = "SELECT * FROM %s WHERE aid=$aid and itype=$itype ORDER BY dtcreate DESC LIMIT $start,$nfetch " % TABLE_ALBUM_IMG

        result = db.query(sqls, vars={"aid": aid, "start": start, "nfetch": nfetch,'itype':itype})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist, total


    def compose_category(self, r):
        category = Category(r['id'],r['code'] ,r['title'])
        category.dtcreate = r['dtcreate']
        category.remark = r['remark']
        category.status = r['status']
        return category

    def compose_album(self, r):
        album = Album(r['id'], r['title'])
        album.dtcreate = r['dtcreate']
        album.remark = r['remark']
        album.status = r['status']
        return album

    def compose_image(self, r):
        image = Image(r['id'], r['title'], r['aid'])
        image.dtcreate = r['dtcreate']
        image.file = r['file']
        image.raw = '/raw'+image.file

        image.thumbnail='/thumb'+image.file
        image.large='/lar'+image.file
        image.medium='/mid'+image.file

        image.itype=r['itype']
        return image

    def addComment(self):
        pass


    def deleteComment(self):
        pass

    def compose_order(self,r):
        order  = Order(r['uid'])
        order.price =r['price']
        order.dtcreate = r['dtcreate']
        order.dtupdate = r['dtupdate']
        order.dtcomplete = r['dtcomplete']

        order.status = r['status']


    def list_orders(self,uid=None):
        sqls = 'SELECT * FROM %s %s ORDER BY dtcreate desc '

        where_condition=''
        if uid:
            where_condition = 'WHERE uid='+uid
        result = db.query((sqls %(TABLE_SITE_ORDER,where_condition)))

        rlist = []

        if result:
            for r in result:
                order = self.compose_order(r)
                rlist.append(order)

    #TODO
    def list_order_imgs(self,oid, status=1):
        sqls = 'SELECT a.* FROM cms_album_img a RIGHT JOIN site_order_img b ON b.iid=a.id WHERE b.oid=%d AND b.status=%d ORDER BY a.dtcreate desc '

        result = db.query((sqls %(oid,status)))

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist

    def update_user_choice(self,iid,oid,status):
        sqls = 'UPDATE site_order_img SET status=%d where oid=%d and iid=%d'

        db.query((sqls %(status,oid,iid)))

    def site_user_login(self,email,passwd):
        sqls = 'select uid,passwd,status from $table where email=$email'
        result = db.query(sqls,vars={'table':TABLE_SITE_USER,'email':email})

        if result:
            for r in result:
                uid = r['uid']
                status = r['status']
                upasswd = r['passwd']

                if status==1:
                    if upasswd == passwd:
                    # if len(upasswd) == len(passwd):
                    #     for i in xrange(0,len(upasswd)):
                    #         if upasswd[i] != passwd[i]:
                    #             return 0,'Invalid Password'

                        return uid,'OK'
                else:
                    return status,'status'

        # not found this email id
        return -1,'NotFound'





