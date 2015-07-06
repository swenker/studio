__author__ = 'wenjusun'

import cgi
import random
import web

from cms.cms_model import Image
from cms import cms_service
from cms import service_config
from wshelper import ServiceHelper
from wshelper import ListWrapper




urls = (
        "/home", "HomePage",
        "/portfolio", "Portfolio",
        "/ga/(\d+)", "GetArticle",
        "/la", "ListArticles",
        "/sc", "School",
        "/news", "News",
        "/service", "Service",
        "/all","ListAllForHomePage",
        "/rpic","RandomPic",
        "/gallery", "AllGallery"
)

app = web.application(urls, globals())
config = service_config.config

t_globals = {
    'datestr': web.datestr,
    'service_config':config
}

render = web.template.render("templates/site", globals=t_globals)

cmsService = cms_service.cmsService

serviceHelper = ServiceHelper()

_EVERY_PAGE = 10


class HomePage():
    def GET(self):
        rlist, total = self.get_all_articles()
        return render.index(rlist, self.get_gallery_imgs())

    def get_gallery_imgs(self):
        start= 0
        nfetch=16
        acode = 'hg'

        # cmsService.get_album_imglist(acode,start,nfetch,itype=Image.IMG_TYPE_HOME_GALLERY)
        plist,ptotal = cmsService.get_album_imglist(acode,start,nfetch)
        return plist
    def get_all_articles(self):

        start = 0
        nfetch = 8
        ctcode = None

        return cmsService.list_articles(start, nfetch,ctcode,query_in_title=None,status=str(1))


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

class ListAllForHomePage():
    def GET(self):
        params = web.input(n=0)

        start = 0
        nfetch = 8
        if params.n :
            nfetch = int(params.n)
        ctcode = None


        rlist, total = cmsService.list_articles(start, nfetch,ctcode,query_in_title=None,status=str(1))


class RandomPic():
    def GET(self):
        start= random.randint(0,10)
        nfetch=4
        acode = 'hg'

        plist,ptotal = cmsService.get_album_imglist(acode,start,nfetch)

        return serviceHelper.to_jsonstr(ListWrapper(plist,total_count=len(plist)))

class AllGallery():
    def GET(self):
        start= 0
        nfetch=16
        acode = 'hg'

        # cmsService.get_album_imglist(acode,start,nfetch,itype=Image.IMG_TYPE_HOME_GALLERY)
        plist,ptotal = cmsService.get_album_imglist(acode,start,nfetch)

        return render.all_gallery(plist,ptotal)

