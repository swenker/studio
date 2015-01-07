__author__ = 'wenju'

import web

from oss import oss_api
from cms_model import *
import service_config
from aliyun_oss_handler import *

TABLE_ARTICLE_META = "cms_article_meta"
TABLE_ARTICLE_CONTENT = "cms_article_content"

TABLE_ALBUM = "cms_album"
TABLE_ALBUM_IMG = "cms_album_img"

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
            sqls = "INSERT INTO %s(title,subtitle,author,source,dtpub,dtcreate,dtupdate,cover,brief,cid) VALUES" \
                   "($title,$subtitle,$author,$source,$dtpub,$dtcreate,$dtupdate,$cover,$brief,$cid)" \
                   % TABLE_ARTICLE_META

            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtpub': article_meta.dtpub, 'dtcreate': time_now, 'dtupdate': time_now,
                           'cover': article_meta.cover, 'brief': article_meta.brief, 'cid': cid}
            )

            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            t.commit()

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

            sqls = "UPDATE %s SET title=$title,subtitle=$subtitle,author=$author,source=$source,dtupdate=$dtupdate,cover=$cover,brief=$brief WHERE id=$oid" \
                   % TABLE_ARTICLE_META

            # logger.debug(sqls)
            db.query(sqls,
                     vars={'title': article_meta.title, 'subtitle': article_meta.subtitle,
                           'author': article_meta.author, 'source': article_meta.source,
                           'dtupdate': get_timenow(), 'cover': article_meta.cover, 'brief': article_meta.brief,
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


    def list_articles(self, start, nfetch, query_in_title=None, status=None):
        """list articles meta without content  """
        sql_total = "SELECT COUNT(*) as total FROM cms_article_meta "

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status FROM " + TABLE_ARTICLE_META

        if query_in_title:
            sqlwhere = " WHERE title LIKE $keywords OR brief LIKE '%" + query_in_title + "%'"
            sqls += sqlwhere

            sql_total += sqlwhere


        # if status:

        sqls += " ORDER BY dtcreate desc "

        sqls += " LIMIT $start,$nfetch"

        total = 0

        if query_in_title:

            result = db.query(sql_total, vars={'keywords': query_in_title})

        else:

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
               "m.dtupdate AS dtupdate,m.dtcreate AS dtcreate,m.cover AS cover,m.brief AS brief,m.cid AS cid,m.status AS status,c.content AS content " \
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

        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status  FROM cms_article_meta where id=$oid"

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

        return article_meta

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
            sqls = "INSERT INTO %s(title,dtcreate,file,aid)VALUES($title,$dtcreate,$file,$aid)" % TABLE_ALBUM_IMG

            db.query(sqls,
                     vars={'title': img.title, 'dtcreate': get_timenow(), 'file': img.file, 'aid': img.aid}
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


    def get_album_imglist(self, aid, start=0, nfetch=20):
        total = 0

        sql_total = "SELECT COUNT(*) as total FROM %s WHERE aid=$aid " % TABLE_ALBUM_IMG

        total_query = db.query(sql_total, vars={'aid': aid})

        if total_query:
            total = total_query[0]['total']

        sqls = "SELECT * FROM %s WHERE aid=$aid ORDER BY dtcreate DESC LIMIT $start,$nfetch " % TABLE_ALBUM_IMG

        result = db.query(sqls, vars={"aid": aid, "start": start, "nfetch": nfetch})

        rlist = []

        if result:
            for r in result:
                img = self.compose_image(r)
                rlist.append(img)

        return rlist, total


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
        image.thumbnail='/thu'+image.file
        image.large='/lar'+image.file

        return image

    def addComment(self):
        pass


    def deleteComment(self):
        pass


def get_timenow():
    return datetime.now().strftime(TIME_FORMAT)


