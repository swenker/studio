__author__ = 'sunwj'

import json

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config



urls=("/p/adm/adminsvc","AdminService",
      "/p/adm/new_article","NewArticle",
      "/p/adm/preview_article","PreviewArticle",
      "/p/adm/delete_article","DeleteArticle",
      "/p/adm/edit_article","EditArticle",
      "/p/adm/list_article","ListEditArticles",
      "/p/pub/get_article/(\d+)","GetArticle",
      "/p/pub/list_article","ListPubArticles",
      "/p/adm/files/(.*)","FilesHandler")


#web.config.debug = False
app=web.application(urls,globals())
application = app.wsgifunc()

#session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates")
config = service_config.config
store_path = config.img_save_path

cgi.maxlen = 10 * 1024 * 1024

cmsService = cms_service.CmsService()
class ServiceHelper():
    def load_config(self):
        pass

    def preview(self):
        pass

    def save(self,params):
        pass

    def publish(self):
        pass

    def saveFile(self,image,store_path):
        #TODO write to oss

        imgpath = image.cover.filename.replace('\\','\\')
        imgname = imgpath.split('/')[-1]
        fout = open(store_path+"/"+imgname,'w')
        fout.write(image.cover.file.read())
        fout.close()
        saved_path=""
        return saved_path

    def compose_article(self,params):
        article_meta = cms_model.ArticleMeta()
        article_meta.id = -1
        article_meta.title = params.title
        article_meta.subtitle = params.subtitle
        article_meta.author = params.author
        article_meta.source = params.source
        #article_meta.dtpub = datetime.now().strftime(TIME_FORMAT)
        #todo auto generate
        article_meta.brief = 'This is brief'
        article_meta.status = 1

        article_content = cms_model.ArticleContent(params.content)
        article = cms_model.ArticleEntity(article_meta,article_content)
        return article


serviceHelper = ServiceHelper()

class AdminService():
    def GET(self):
        action = web.input('uaction')
        key = web.input('key',None)
        if action == 'reset':
            serviceHelper.load_config()

        elif action == 'listconfig':
            #TODO
            pass


class UploadImage():
    def POST(self):
        imgpath=''
        image =web.input(imgfile={})
        if 'imgfile' in image :
            imgpath = serviceHelper.saveFile(image,store_path)

        return imgpath

class NewArticle():
    def GET(self):
        return render.article_form()

    def POST(self):
        uaction = web.input("uaction")

        print "uaction:"+uaction
        #try:
        #    image = web.input(cover={})
        #    if 'cover' in image and image:
        #        serviceHelper.saveFile(image,store_path)
        #    cmsService.new_article(serviceHelper.compose_article(web.input))
        #
        #except ValueError:
        #    return "File Limit is 10MB."

        if uaction == 'save':

            cmsService.new_article(serviceHelper.compose_article(web.input()))

        elif uaction == 'preview':
            serviceHelper.save(web.input())
            serviceHelper.preview()

        elif uaction == 'publish':
            serviceHelper.publish()


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

        return to_jsonstr(ListWrapper(rlist,total,total_pages))

class PreviewArticle():
    def GET(self):
        params = web.input()
        aid = params.aid

        if aid :
            return

class GetArticle():
    def GET(self,id):
        article = cmsService.get_article(id)
        if article:
            return to_jsonstr(article)
        else:
            return render.common("failed:"+str(id))

class FilesHandler():
    def GET(self):
        #web.seeother()
        pass

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
