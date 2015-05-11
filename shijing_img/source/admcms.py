__author__ = 'sunwj'

import json

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
import wshelper


urls = ("/adminsvc", "AdminService",
        "", "Dashboard",
        "/login", "LoginService",
        "/new_article", "NewArticle",
        "/save_article", "SaveArticle",
        "/preview_article", "PreviewArticle",
        "/delete_article", "DeleteArticle",
        "/edit_article", "EditArticle",
        "/list_article", "ListEditArticles",
        "/list_column", "ListEditArticles",
        "/new_column", "ListEditArticles",
        "/edit_column", "ListEditArticles",
        "/delete_column", "ListEditArticles",
        "/album", "EditAlbum",
        "/list_album", "ListAlbums",
        "/upload_img", "UploadImage",
        "/list_imgs", "ListImages",
        "/delete_img", "DeleteImage",
        "/select_imgs", "SelectImages",
        "/select_cover", "SelectCover")

t_globals = {
    'datestr': web.datestr
}

# web.config.debug = FalseListImages
app = web.application(urls, globals())
#application = app.wsgifunc()

# session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates/adm", globals=t_globals)
config = service_config.config

cgi.maxlen = 2 * 1024 * 1024

cmsService = cms_service.CmsService()

serviceHelper = wshelper.ServiceHelper()


class LoginService():
    def GET(self):
        return render.login('')

    def POST(self):
        params = web.input()
        email = params.email
        passwd = params.passwd

        print "abc:"+email,passwd
        if email and passwd:
            if email == 'abctest@126.com' and passwd=='onecase':
                #TODO save session?
                return web.seeother("/p/adm")

            else:

                return render.login("Failed")
        else:
            return render.login("Please Input email and password")

#TODO
class AdminService():
    def GET(self):
        action = web.input('uaction')
        if action == 'reset':
            serviceHelper.load_config()

        elif action == 'listconfig':
            # TODO
            pass


class Dashboard:
    def GET(self):
        return render.dashboard()


class NewArticle():
    def GET(self):
        return render.article_form(None,None)


class SaveArticle():
    def POST(self):

        params = web.input(subtitle=None,oid=None,cid=None)
        if not params.oid:
            cmsService.new_article(serviceHelper.compose_article(params))

        else:
            cmsService.update_article(serviceHelper.compose_article(params))

        return render.common("OK")


_EVERY_PAGE = 10


class ListEditArticles():
    def GET(self):
        params = web.input(np=0, kw=None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()

        rlist, total = cmsService.list_articles(start, nfetch, query_in_title=keyword)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.article_list_edit(rlist, total, total_pages,npages)


# TODO
class PreviewArticle():
    def GET(self, id):
        article = cmsService.get_article(id)
        if article:
            return to_jsonstr(article)
        else:
            return render.common("failed:" + str(id))


class DeleteArticle():
    def GET(self):
        id = web.input().id
        cmsService.delete_article(id)

        return render.common("deleted:" + str(id))


class EditArticle():
    def GET(self):
        id = web.input().id
        article = cmsService.get_article(id)
        if article:
            return render.article_form(article.article_meta, article.article_content)
        else:
            return render.common("failed:" + str(id))


class UploadImage:
    def GET(self):
        return render.image()

    def POST(self):
        try:
            image_data = web.input(file={})
            if image_data and 'file' in image_data:
                imgmeta = cms_model.Image(image_data.aid)
                imgmeta.aid = 1

                # TODO title field
                imgmeta.title,imgmeta.file = serviceHelper.store(image_data)

                cmsService.create_img(imgmeta)
            return render.common("OK")

        except ValueError:
            return "File Limit is 1MB."

class DeleteImage():
    "idlist=id separated by ,"
    def GET(self):
        idlist = web.input().id
        cmsService.delete_img(idlist)

        return web.seeother("/list_imgs?aid=1")


class ListImages:
    def GET(self):
        params = web.input(np=0,aid=1)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        aid = params.aid

        rlist, total = cmsService.get_album_imglist(aid,start, nfetch)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_list_edit(rlist, total, total_pages,npages,config)

class SelectImages:
    def GET(self):
        params = web.input(np=0,aid=1)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        aid = params.aid

        rlist, total = cmsService.get_album_imglist(aid,start, nfetch)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_list_selector(rlist, total, total_pages,npages,config)

class SelectCover:
    def GET(self):
        params = web.input(np=0,aid=1)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        aid = params.aid

        rlist, total = cmsService.get_album_imglist(aid,start, nfetch)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_cover_selector(rlist, total, total_pages,npages,config)


class ListWrapper:
    def __init__(self, rlist, total_count, total_pages):
        self.rlist = rlist
        self.total = total_count
        self.total_pages = total_pages

    def jsonable(self):
        return self.__dict__


def to_jsonstr(obj):
    return json.dumps(obj.__dict__, cls=cms_model.ComplexEncoder)


