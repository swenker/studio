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
        "/ga/(\d+)", "GetArticle",
        "/la", "ListArticles",
        "/sc", "School",
        "/news", "News",
        "/service", "Service",
        "/list_imgs", "ListImages"
)

app = web.application(urls, globals())
config = service_config.config

t_globals = {
    'datestr': web.datestr,
    'service_config':config
}

render = web.template.render("templates/site", globals=t_globals)

cmsService = cms_service.cmsService

serviceHelper = wshelper.ServiceHelper()

_EVERY_PAGE = 10


class HomePage():
    def GET(self):

        return render.index()

class Portfolio():
    def GET(self):

        ctcode = config.ctcode_portfolio

        rlist, total = cmsService.list_articles(0, 1,ctcode,None,status=str(1))
        lista = rlist[0]

        article = cmsService.get_article(lista.oid)

        if article:
            return render.portfolio(article.article_meta, article.article_content)

        else:
            return render.common("failed:" + str(id))

class Service():
    def GET(self):
        params = web.input(np=0, kw=None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()

        ctcode = config.ctcode_service

        rlist, total = cmsService.list_articles(start, nfetch,ctcode,query_in_title=keyword,status=str(1))

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        return render.service(rlist, total, total_pages,npages)

class School():
    def GET(self):
        params = web.input(np=0, kw=None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()

        ctcode = config.ctcode_school
        rlist, total = cmsService.list_articles(start, nfetch,ctcode,query_in_title=keyword,status=str(1))

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        return render.school(rlist, total, total_pages,npages)

class News():
    def GET(self):
        params = web.input(np=0, kw=None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()

        ctcode = config.ctcode_news
        rlist, total = cmsService.list_articles(start, nfetch,ctcode,query_in_title=keyword,status=str(1))

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.news(rlist, total, total_pages,npages)


class GetArticle():
    def GET(self, id):
        article = cmsService.get_article(id)
        if article:
            return render.article(article.article_meta, article.article_content)

        else:
            return render.common("Not Found:" + str(id))

class ListArticles():
    def GET(self):
        params = web.input(np=0, kw=None,ctcode= None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()


        if not params.ctcode:
            ctcode = config.ctcode_article
        else :
            ctcode = params.ctcode


        rlist, total = cmsService.list_articles(start, nfetch,ctcode,query_in_title=keyword,status=str(1))

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.article_list(rlist, total, total_pages,npages)



class ListImages():
    def GET(self):
        params = web.input(np=0, kw=None,aid=None)
