__author__ = 'samsung'

import web

from cms_model import *
import service_config

TABLE_ARTICLE_META = "cms_article_meta"
TABLE_ARTICLE_CONTENT = "cms_article_content"

config = service_config.config
logger = config.getlogger("CmsService")

#db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd, charset="UTF-8")
db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd)


class CmsService:
    def __init__(self):
        pass

    def new_article(self, article):
        if article and article.article_meta.id >0:
            logger.error("should go to update with id:" % article.id)
            return
        article_meta = article.article_meta

        t = db.transaction()
        try:
            sqls = "INSERT INTO %s(content)VALUES('%s') " % (TABLE_ARTICLE_CONTENT,article.article_content.content)

            db.query(sqls)

            result = db.query("select LAST_INSERT_ID() AS mid ")
            cid = -1
            if result:
                cid = result[0]['mid']

            time_now = datetime.now().strftime(TIME_FORMAT)
            sqls = "INSERT INTO %s(title,subtitle,author,source,dtpub,dtcreate,cover,brief,cid) VALUES('%s','%s','%s','%s','%s','%s','%s','%s',%d)" \
                  % (TABLE_ARTICLE_META, article_meta.title, article_meta.subtitle, article_meta.author, article_meta.source,
            article_meta.dtpub, time_now, article_meta.cover, article_meta.brief, cid)

            logger.debug(sqls)
            db.query(sqls)

            result = db.query("select LAST_INSERT_ID() AS mid ")
            mid = -1
            if result:
                mid = result[0]['mid']
            t.commit()

            logger.info("articleId [%d] is created" %mid)
            return mid

        except Exception, e:
            print (e)
            t.rollback()
            return -1


    def delete_article(self, mid, hard=False):
        if not hard:
            sqls = "UPDATE %s SET `status`=%d where mid=%d" % (TABLE_ARTICLE_META, 2, mid)
        else:
            sqls = "DELETE FROM %s WHERE id=%d" % (TABLE_ARTICLE_META,mid)
        db.query(sqls)

    def disable_article(self,mid):
        sqls = "UPDATE %s SET `status`=%d where id=%d" % (TABLE_ARTICLE_META, 0, mid)
        db.query(sqls)

    def enable_article(self,mid):
        sqls = "UPDATE %s SET `status`=%d where id=%d" % (TABLE_ARTICLE_META, 1, mid)
        db.query(sqls)


    def list_articles(self, start, nfetch, query_in_title=None,status=None):
        """list articles meta without content  """
        sql_total = "SELECT COUNT(*) as total FROM cms_article_meta "
        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status FROM " + TABLE_ARTICLE_META

        if query_in_title:
            sqlwhere = " WHERE title LIKE '%" + query_in_title + "%' OR brief LIKE '%" + query_in_title + "%'"
            sqls += sqlwhere
            sql_total += sqlwhere


        #if status:

        sqls += " ORDER BY dtcreate desc "

        sqls += " LIMIT %d,%d" % (start, nfetch)


        total = 0
        result = db.query(sql_total)
        if result:
            total = result[0]['total']
        logger.debug("total:"+str(total))

        logger.debug(sqls)
        result = db.query(sqls)

        rlist = []
        if result:
            for r in result:
                article_meta = self.compose_article_meta(r)
                print article_meta
                rlist.append(article_meta)

        return rlist, total

    def get_article(self,id):
        sqls = "SELECT m.id AS id,m.title AS title,m.subtitle AS subtitle,m.author AS author,m.source AS source,m.dtpub AS dtpub," \
               "m.dtupdate AS dtupdate,m.dtcreate AS dtcreate,m.cover AS cover,m.brief AS brief,m.cid AS cid,m.status AS status,c.content AS content " \
               "FROM cms_article_meta m left join cms_article_content c on m.cid=c.id and m.id="+str(id)

        logger.debug(sqls)
        result = db.query(sqls)
        if result:
            r = result[0]
            article_meta = self.compose_article_meta(r)
            article_content = ArticleContent(r['content'])
            article_content.id = r['cid']

            article = ArticleEntity(article_meta,article_content)

            return article

    def get_article_meta(self,id):
        sqls = "SELECT id,title,subtitle,author,source,dtpub,dtupdate,dtcreate,cover,brief,cid,status  FROM cms_article_meta where id="+str(id)

        result = db.query(sqls)
        if result:
            r = result[0]
            article_meta = self.compose_article_meta(r)

            return article_meta

    def get_article_content(self,id):
        sqls = "SELECT content FROM cms_article_content where id="+str(id)

        result = db.query(sqls)
        if result:
            r = result[0]
            article_content = ArticleContent(r['content'])
            article_content.id = id

            return article_content

    def compose_article_meta(self,r):
        article_meta = ArticleMeta()
        article_meta.id = r['id']
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


    def addComment(self):
        pass


    def deleteComment(self):
        pass



