__author__ = 'wenjusun'

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
import wshelper


urls = (
        "/home", "HomePage",
        "/portfolio", "Portfolio",
        "/get_article/(\d+)", "GetArticle",
        "/list_article", "ListArticles",
        "/list_imgs", "ListImages"
)

app = web.application(urls, globals())

t_globals = {
    'datestr': web.datestr
}

render = web.template.render("templates/site", globals=t_globals)
config = service_config.config

cmsService = cms_service.CmsService()

serviceHelper = wshelper.ServiceHelper()

_EVERY_PAGE = 10


class HomePage():
    def GET(self):

        return render.index()

class Portfolio():
    def GET(self):
        params = web.input(ctid= None)

        if not params.ctid:
            ctid = str(1)
        else :
            ctid = params.ctid

        rlist, total = cmsService.list_articles(0, 1,ctid,None,status=str(1))
        lista = rlist[0]

        article = cmsService.get_article(lista.oid)

        if article:
            return render.portfolio(article.article_meta, article.article_content)

        else:
            return render.common("failed:" + str(id))


class GetArticle():
    def GET(self, id):
        article = cmsService.get_article(id)
        if article:
            return render.article(article.article_meta, article.article_content)

        else:
            return render.common("failed:" + str(id))

class ListArticles():
    def GET(self):
        params = web.input(np=0, kw=None,ctid= None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()


        if not params.ctid:
            ctid = str(4)
        else :
            ctid = params.ctid


        rlist, total = cmsService.list_articles(start, nfetch,ctid,query_in_title=keyword,status=str(1))

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.article_list(rlist, total, total_pages,npages)


class ListImages():
    def GET(self):
        params = web.input(np=0, kw=None,aid=None)
