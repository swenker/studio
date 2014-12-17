__author__ = 'sunwj'

import os
import json

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
import wshelper


urls=("/p/adm/adminsvc","AdminService",
      "/p/adm","Dashboard",
      "/p/adm/new_article","NewArticle",
      "/p/adm/save_article","SaveArticle",
      "/p/adm/preview_article","PreviewArticle",
      "/p/adm/delete_article","DeleteArticle",
      "/p/adm/edit_article","EditArticle",
      "/p/adm/list_article","ListEditArticles",
      "/p/adm/list_column","ListEditArticles",
      "/p/adm/new_column","ListEditArticles",
      "/p/adm/edit_column","ListEditArticles",
      "/p/adm/delete_column","ListEditArticles",
      "/p/adm/album","EditAlbum",
      "/p/adm/list_album","ListAlbums",
      "/p/adm/upload_img","UploadImage",
      "/p/adm/list_imgs","ListImages",

      "/p/pub/get_article/(\d+)","GetArticle",
      "/p/pub/list_article","ListPubArticles",
      "/p/adm/files/(.*)","FilesHandler")

t_globals = {
    'datestr':web.datestr
}

#web.config.debug = False
app=web.application(urls,globals())
application = app.wsgifunc()

#session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates",globals=t_globals)
config = service_config.config
store_path = config.img_save_path

cgi.maxlen = 1 * 1024 * 1024

cmsService = cms_service.CmsService()


serviceHelper = wshelper.ServiceHelper()

class AdminService():
    def GET(self):
        action = web.input('uaction')
        key = web.input('key',None)
        if action == 'reset':
            serviceHelper.load_config()

        elif action == 'listconfig':
            #TODO
            pass

class Dashboard:
    def GET(self):
        return render.dashboard()

class NewArticle():
    def GET(self):
        return render.article_form(None)

class SaveArticle():

    def POST(self):
        #try:
        #    image = web.input(cover={})
        #    if 'cover' in image and image:
        #        serviceHelper.saveFile(image,store_path)
        #    cmsService.new_article(serviceHelper.compose_article(web.input))
        #
        #except ValueError:
        #    return "File Limit is 10MB."

        params = web.input(subtitle=None)
        if not params.id:
            cmsService.new_article(serviceHelper.compose_article(params))

        else:
            cmsService.update_article(serviceHelper.compose_article(params))


        return render.common("OK")




_EVERY_PAGE = 20

class ListEditArticles():
    def GET(self):
        params = web.input(np=0,kw=None)

        npages=int(params.np)
        start=(npages)*_EVERY_PAGE
        nfetch =_EVERY_PAGE

        keyword=params.kw
        if keyword:
            keyword = keyword.strip()

        rlist=None

        rlist,total = cmsService.list_articles(start,nfetch)

        total_pages=(total+_EVERY_PAGE-1)/_EVERY_PAGE

        #return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.article_list_edit(rlist,total,total_pages)

#TODO
class PreviewArticle():
    def GET(self,id):
        article = cmsService.get_article(id)
        if article:
            return to_jsonstr(article)
        else:
            return render.common("failed:"+str(id))

class GetArticle():
    def GET(self,id):
        article = cmsService.get_article(id)
        if article:
            return to_jsonstr(article)
        else:
            return render.common("failed:"+str(id))

class DeleteArticle():
    def GET(self):
        id = web.input().id
        article = cmsService.delete_article(id)

        if article:
            return to_jsonstr(article)
        else:
            return render.common("failed:"+str(id))

class EditArticle():
    def GET(self):
        id = web.input().id
        article = cmsService.get_article(id)
        if article:
            return render.article_form(article.article_meta,article.article_content)
        else:
            return render.common("failed:"+str(id))

class UploadImage:
    def GET(self):
        return render.image()

    def POST(self):
        try:
           image_data = web.input(file={})
           if image_data and 'file' in image_data:
               imgmeta = cms_model.Image(image_data.aid)
               imgmeta.aid=1

               #TODO title field

               imgmeta.file=serviceHelper.saveFile(image_data,store_path)
               cmsService.create_img(imgmeta)
           return render.common("OK")

        except ValueError:
           return "File Limit is 1MB."



class ListWrapper:
    def __init__(self,rlist,total_count,total_pages):
        self.rlist=rlist
        self.total = total_count
        self.total_pages=total_pages

    def jsonable(self):
        return self.__dict__


def to_jsonstr(obj):
    return json.dumps(obj.__dict__,cls=cms_model.ComplexEncoder)


#It can not be run on Windows
if __name__=="__main__":
    app.run()
