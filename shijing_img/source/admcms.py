

__author__ = 'sunwj'


import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
from cms import batch_image_handler

from wshelper import ServiceHelper
from wshelper import ListWrapper



urls = ("/adminsvc", "AdminService",
        "", "Dashboard",
        "/", "Dashboard",
        "/login", "LoginService",
        "/new_article", "NewArticle",
        "/save_article", "SaveArticle",
        "/preview_article", "PreviewArticle",
        "/delete_article", "DeleteArticle",
        "/edit_article", "EditArticle",
        "/list_article", "ListEditArticles",
        "/list_category", "ListCategories",
        # "/new_category", "NewCategory",
        # "/save_category", "SaveCategory",
        # "/edit_category", "EditCategory",
        # "/delete_category", "DeleteCategory",
        "/album", "EditAlbum",
        "/list_album", "ListAlbums",
        "/upload_img", "UploadImage",
        "/list_imgs", "ListImages",
        "/delete_img", "DeleteImage",
        "/select_imgs", "SelectImages",
        "/select_cover", "SelectCover",
        "/refresh","RefreshHomePage",
        "/orders", "ListOrders",
        "/order/form","HandlerOrderForm",
        "/order/delete","DeleteOrder",
        "/loadfolder","LoadFolder",
        "/signout", "Signout",
        "/listimgs/(\d+)", "ListOrderImages",
        "/okimgs/(\d+)", "ListSelectedImages",
        "/yy", "ListPreorder",
        "/yydelete/(\d+)", "DeletePreorder",
        "/siteuser/new","SiteUserHandler"
        )

config = service_config.config

t_globals = {
    'datestr': web.datestr,
    'service_config':config
}

#print web.config.debug #default is True
web.config.debug = False
app = web.application(urls, globals())

render = web.template.render("templates/adm", globals=t_globals)

cgi.maxlen = config.img_size_limit * 1024 * 1024

cmsService = cms_service.cmsService

serviceHelper = ServiceHelper()
adm_session = serviceHelper.init_adm_session(web,app)
web.config.session_parameters['timeout'] = 8000

logger = config.getlogger()
logger.info('admincms initialized')


def my_loadhook():
    request_uri = web.ctx.environ.get('REQUEST_URI')
    # print adm_session.get('admin')
    if not adm_session.get('admin') and request_uri != '/p/adm/login':
        web.seeother('/login')

def my_unloadhook():
    #print "my unload hook"
    pass

app.add_processor(web.loadhook(my_loadhook))
app.add_processor(web.unloadhook(my_unloadhook))


class LoginService():
    def GET(self):
        return render.login('')

    def POST(self):
        params = web.input()
        email = params.email
        passwd = params.passwd

        if email and passwd:
            if email == 'abctest@126.com' and passwd=='onecase':
                adm_session.admin = True
                return web.seeother("/")

            else:
                return render.login("Failed")
        else:
            return render.login("Please Input email and password")

class Signout():
    def GET(self):
        adm_session.kill()
        return web.seeother("/login")


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

        params = web.input(subtitle=None,oid=None,cid=None,ctcode=[])
        if not params.oid:
            cmsService.new_article(serviceHelper.compose_article(params))

        else:
            cmsService.update_article(serviceHelper.compose_article(params))

        serviceHelper.generateIndexHtml()

        web.seeother('list_article?ctcode='+params.ctcode[0])


_EVERY_PAGE = config.nevery_page


class ListEditArticles():
    def GET(self):
        params = web.input(np=0, kw=None,ctcode=None)

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        ctcode = params.ctcode

        keyword = params.kw
        if keyword:
            keyword = keyword.strip()

        rlist, total = cmsService.list_articles(start, nfetch,ctcode, query_in_title=keyword)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.article_list_edit(rlist, total, total_pages,npages,ctcode)


# TODO
class PreviewArticle():
    def GET(self, id):
        article = cmsService.get_article(id)
        if article:
            return serviceHelper.to_jsonstr(article)
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


class RefreshHomePage():
    def GET(self):
        serviceHelper.generateIndexHtml()
        web.seeother('/')



# class NewCategory():
#     def GET(self):
#         return render.category_form(None,None)
#
# class SaveCategory():
#     def POST(self):
#
#         params = web.input(oid=None,title=None,code=None,cid=None)
#         if not params.oid:
#             cmsService.create_category(serviceHelper.compose_category(params))
#
#         else:
#             cmsService.update_category(serviceHelper.compose_category(params))
#
#         return render.common("OK")
#
# class DeleteCategory():
#     def GET(self):
#         id = web.input().id
#         cmsService.delete_category(id)
#
#         return render.common("deleted:" + str(id))
#
# class EditCategory():
#     def GET(self):
#         id = web.input().id
#         category = cmsService.get_category(id)
#         if category:
#             return render.category_form(category.category_meta, category.category_content)
#         else:
#             return render.common("failed:" + str(id))

class ListCategories():
    def GET(self):
        rlist = cms_service.category_map.values()

        serviceHelper.set_common_header(web)
        return serviceHelper.to_jsonstr(ListWrapper(rlist))

class ListAlbums():
    def GET(self):

        params = web.input(format=None)
        rlist = cms_service.album_map.values()

        if params.format and 'json'== params.format:

            serviceHelper.set_common_header(web)
            return serviceHelper.to_jsonstr(ListWrapper(rlist))

        else:
            return render.album_list_edit(rlist)



class UploadImage:
    def GET(self):
        return render.image()

    def POST(self):
        try:
            image_data = web.input(file={})
            if image_data and 'file' in image_data:
                imgmeta = cms_model.Image()
                imgmeta.aid = cms_service.album_map.get(image_data.acode).oid

                imgmeta.code = image_data.acode

                try:
                    imgmeta.title,imgmeta.file = serviceHelper.store(image_data)
                    cmsService.create_img(imgmeta)
                    return render.common("OK")
                except StandardError,e:
                    return render.common("Failed:"+e.message)

        except ValueError:
            return "File Limit is 1MB."

    #Not used now
    def POST1(self):
        try:
            image_data = web.input(file=[{}])

            if image_data and 'file' in image_data:
                #image_data['file']

                imgmeta = cms_model.Image(image_data.aid)
                imgmeta.aid = 1

                # TODO title field
                imglist = serviceHelper.store_list(image_data)

                cmsService.create_imglist(imgmeta.aid,imglist)

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
        params = web.input(np=0,acode='ac')

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE

        acode = params.acode

        rlist, total = cmsService.get_album_imglist(acode,start, nfetch)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_list_edit(rlist, total, total_pages,npages,acode)

class SelectImages:
    def GET(self):
        params = web.input(np=0,acode='ac')

        npages = int(params.np)
        start = npages * _EVERY_PAGE
        nfetch = _EVERY_PAGE


        acode = params.acode

        rlist, total = cmsService.get_album_imglist(acode,start, nfetch)

        total_pages = (total + _EVERY_PAGE - 1) / _EVERY_PAGE

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_list_selector(rlist, total, total_pages,npages)

class SelectCover:
    def GET(self):
        local_every_page = _EVERY_PAGE * 1
        params = web.input(np=0,acode='ac')

        npages = int(params.np)
        start = npages * local_every_page
        nfetch = local_every_page

        acode = params.acode

        rlist, total = cmsService.get_album_imglist(acode,start, nfetch)

        total_pages = (total + local_every_page - 1) / local_every_page

        # return to_jsonstr(ListWrapper(rlist,total,total_pages))
        return render.img_cover_selector(rlist, total, total_pages,npages)

class LoadFolder():
    def GET(self):

        return render.load_folder()

    def POST(self):
        params = web.input()
        folder = params.folder

        orderid = int(params.orderid)

        counter = batch_image_handler.load_local_folder(folder,cms_service.album_map.get('oa').oid,orderid)
        #web.seeother('/listimgs/'+str(orderid))
        return render.common("Uploaded %d,<a href='/p/u/listimgs/%d'> check it</a>" %counter,orderid)

class ListOrders():
    def GET(self):
        params = web.input(uid = None)

        uid = None
        if params.uid:
            uid = int(params.uid)

        rlist = cmsService.list_orders(uid)

        return render.order_list(rlist, len(rlist))


class ListOrderImages():
    "List all images of for the order"
    def GET(self,oid):

        rlist = cmsService.list_order_imgs(int(oid))
        # print len(rlist)
        return render.img_list_select(rlist, len(rlist),oid)

class ListSelectedImages():
    def GET(self,oid):
        rlist = cmsService.list_selected_imgs(int(oid))

        return render.img_select_result(rlist, len(rlist),oid)

class ListPreorder():
    def GET(self):
        status = None
        rlist = cmsService.list_preorder(status)
        return render.yuyue_list(rlist)

class DeletePreorder():
    def GET(self,oid):

        cmsService.delete_preorder(int(oid))
        return  render.common("deleted")

class HandlerOrderForm():
    def GET(self):
        params = web.input(oid=None,porder=None)
        oid = params.oid
        order = None
        if oid:
            order = cmsService.load_order(int(oid))
        else:
            porder = params.porder
            print params
            if porder:
                order = cms_model.Order(None)
                order.dttake = params.dttake
                order.remark = params.remark
                order.title = params.utitle

                order.price = 999.00
                order.total_limit = 120
                order.edit_limit = 30


        return render.order_form(order)

    def POST(self):
        params = web.input(oid=None,dtcomplete=None)

        order = serviceHelper.compose_order(params)
        oid = cmsService.save_order(order)

        return render.common("Order Saved,<a href='?oid="+str(oid)+"'>return</a>")

class DeleteOrder():
    def GET(self):
        params = web.input(oid=None)
        ops_result = "OK"
        if(params.oid):
            cmsService.delete_order(int(params.oid))

        else:
            ops_result = "id is needed"

        return render.common(ops_result)


class SiteUserHandler():
    def GET(self):
        params = web.input()
        mobile = params.mobile
        poid = int(params.poid)
        siteuser = cms_model.SiteUser(passwd='abcd1234',mobile=mobile)
        siteuser.email=''

        try:
            uid = cmsService.create_siteuser(siteuser)
            cmsService.update_porder_status(poid,uid,2)
            return "{\"status\":\"OK\"}"
        except BaseException,e:
            return e