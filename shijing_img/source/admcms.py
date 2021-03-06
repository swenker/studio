

__author__ = 'sunwj'

from zipfile import ZipFile
import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
from cms import batch_image_handler
from cms import cms_utils


from wshelper import ServiceHelper
from wshelper import ListWrapper


#TODO move this to a config file or a separated file
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
        "/album/list", "ListAlbums",
        "/img/upload", "UploadImage",
        "/img/list", "ListImages",
        "/img/delete", "DeleteImages",
        "/img/move2newalbum", "MoveToNewAlbum",
        "/img/select", "SelectImages",
        "/img/cover/select", "SelectCover",
        "/refresh","RefreshHomePage",
        "/orders", "ListOrders",
        "/order/form","HandleOrderForm",
        "/order/delete","DeleteOrder",
        "/order/(\d+)","GetOrder",
        "/loadfolder","LoadFolder",
        "/order/loadphoto","LoadOrderPhoto",
        "/order/jobstatus/(\d+)","GetOrderJobStatus",
        "/signout", "Signout",
        "/listimgs/(\d+)", "ListOrderImages",
        "/okimgs/(\d+)", "ListSelectedImages",
        "/yy", "ListPreorder",
        "/yydelete/(\d+)", "DeletePreorder",
        "/siteuser/createform","CreateSiteUserHandler",
        "/siteuser/create","CreateSiteUserHandler",
        "/siteuser/new","NewSiteUserHandler",
        "/siteuser/list","SiteUserList",
        "/siteuser/save","SaveSiteUser",
        "/siteuser/(\d+)","GetSiteUser",
        "/siteuser/delete/(\d+)","DeleteSiteUser",
        "/siteuser/resetpwd/(\d+)","ResetSiteUserPassword",
        "/download_simglist/(\d+)","DownloadSelectedImageResult",
        "/order/status","ChangeOrderStatus",
        "/order/imgcover/(\d+)","GetOrderImageCover",
        "/total","TotalCounterHandler"
        )

config = service_config.config

#Thus the variables can be used within pages.
t_globals = {
    'datestr': web.datestr,
    'daystr': cms_utils.daystr,
    'service_config':config,
    'str':str
}

#print web.config.debug #default is True
web.config.debug = config.web_debug
app = web.application(urls, globals())

render = web.template.render("templates/adm", globals=t_globals)

#upload order photos?
cgi.maxlen = config.img_size_limit * 1024 * 1024 *10

cmsService = cms_service.cmsService

serviceHelper = ServiceHelper()
adm_session = serviceHelper.init_adm_session(web, app)
web.config.session_parameters['timeout'] = 8000

logger = config.getlogger("admcms")

_EVERY_PAGE = config.nevery_page

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


""" -----------------Thread----------------------------  """

job_service = batch_image_handler.JobService()


logger.info('admincms initialized')

class LoginService():
    "Admin login handler"
    def GET(self):
        return render.login('')

    def POST(self):
        params = web.input()
        email = params.email
        passwd = params.passwd

        #TODO put into db
        if email and passwd:
            if email == 'abctest@126.com' and passwd=='onecase':
                adm_session.admin = True
                logger.info("[%s] logged in" % email)
                return web.seeother("/")

            else:
                logger.info("[%s] logged failed" % email)
                return render.login("Failed")
        else:
            return render.login("Please Input email and password")

class Signout():
    def GET(self):
        adm_session.kill()
        #TODO username
        #logger.info("[%s] logged in" % adm_session.get)
        return web.seeother("/login")


#TODO enable service manageable on web console
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


# TODO implement this feature
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

class DeleteImages():
    def GET(self):
        iid = int(web.input().iid)
        order_id = web.input().oid
        cmsService.delete_img(iid)

        return web.seeother('/listimgs/'+str(order_id))

    "idlist=id separated by ,"
    def POST(self):
        idlist = web.input().idlist
        if idlist and len(idlist)>1:
            cmsService.delete_imglist(idlist)

        return web.seeother("/img/list?aid=1")

class MoveToNewAlbum():
    def POST(self):
        idlist = web.input().idlist
        new_acode = web.input().nacode

        if new_acode and idlist and len(idlist)>1:
            cmsService.move_imglist_to_album(idlist,new_acode)

        return web.seeother("/img/list?aid=1")

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

        counter = batch_image_handler.load_local_folder(cms_service.album_map.get('oa').oid,folder,orderid)
        #web.seeother('/listimgs/'+str(orderid))
        return render.common("Uploaded %d,<a href='/p/adm/listimgs/%d'> check it</a>" %(counter,orderid))

"New implementation:asynchronization"

class LoadOrderPhoto():
    def GET(self):
        params = web.input()
        oid = 0
        if params.oid:
            oid = int(params.oid)
        return render.load_order_photo(oid)

    def POST(self):
        try:
            params = web.input(photozip={})
            if params and 'photozip' in params:

                folder = params.folder
                if not folder.startswith('/'):
                    folder='/'+folder

                orderid = int(params.orderid)
                zipname = params.photozip.filename.replace('\\', '\\')

                #print "----" +str(orderid)
                #print "----" +zipname

                base_store_path = config.img_save_path
                raw_relative_dir="/raw"+folder
                raw_full_store_dir = "%s%s" % (base_store_path, raw_relative_dir)

                import os
                if not os.path.exists(raw_full_store_dir):
                    try:
                        os.makedirs(raw_full_store_dir)
                    except OSError:
                        pass

                #Save zip to temp file
                tmp_zip_file = "/tmp/"+zipname
                tmp_zip_fout = open(tmp_zip_file,'w')
                tmp_zip_fout.write(params.photozip.file.read())
                tmp_zip_fout.close()

                photo_zip = ZipFile(tmp_zip_file,'r')
                photo_zip.extractall(raw_full_store_dir)
                photo_zip.close()

                logger.info("%s uploaded" %tmp_zip_file)
                #TODO using new thread? how to update web view?
                # counter = batch_image_handler.load_local_folder(cms_service.album_map.get('oa').oid,folder,orderid)

                photo_job = cms_model.PhotoJob(orderid,folder,cms_service.album_map.get('oa').oid)

                job_id = job_service.submit_job(cms_model.Job("PhotoJob",photo_job))

                return job_id

                # return render.common("Uploaded %d,<a href='/p/adm/listimgs/%d'> check it</a>" %(counter,orderid))
            else:
                return render.common("Uploaded nothing" )

        except StandardError as se:
            logger.exception(se)
            return render.common("Failed:%s " %se)

class GetOrderJobStatus():
    def GET(self,job_id):
        job_id = int(job_id)

        return job_service.get_job_status(job_id)


class ListOrders():
    def POST(self):
        params = web.input(uid = None,status=None)
        uid = None
        status = None
        if params.uid:
            uid = int(params.uid)
        if params.status:
            status = int(params.status)
        rlist = cmsService.list_orders_bystatus(status,uid)

        return render.order_list(rlist, len(rlist))

    def GET(self):
        params = web.input(uid = None)
        if params.uid:
            uid = int(params.uid)
            rlist = cmsService.list_orders(uid)
        else:
            rlist = cmsService.list_orders_uncompleted()

        return render.order_list(rlist, len(rlist))


class ListOrderImages():
    "List all images of for the order"
    def GET(self,oid):
        rlist = cmsService.list_order_imgs(int(oid))
        # print len(rlist)
        return render.img_list_select(rlist, len(rlist), oid)


class ListSelectedImages():
    def GET(self,oid):
        rlist = cmsService.list_selected_imgs(int(oid))

        return render.img_select_result(rlist, len(rlist), oid)


class ListPreorder():
    def GET(self):
        status = None
        rlist = cmsService.list_preorder(1,status)
        return render.yuyue_list(rlist)


class DeletePreorder():
    def GET(self,oid):
        cmsService.delete_preorder(int(oid))
        return  render.common("deleted")


class HandleOrderForm():
    def GET(self):
        params = web.input(oid=None,porder=None,uid=None)
        oid = params.oid
        order = None
        uid = params.uid
        if oid:
            order = cmsService.load_order(int(oid))
        else:
            order = cms_model.Order(None)
            porder = params.porder
            # print params
            if porder:
                order.dttake = params.dttake
                order.remark = params.remark
                order.title = params.utitle

            else:
                order.uid = uid
                order.price = 999.00
                order.total_limit = 120
                order.edit_limit = 30

        return render.order_form(order)


    def POST(self):
        params = web.input(oid=None)

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

class GetOrder():
    def GET(self, oid):

        order_id = int(oid)
        order = cmsService.load_order(order_id)

        # return '{"name":"'+order.title+'"}'
        return order.title


class NewSiteUserHandler():
    "Create user from pre-order"
    def GET(self):
        params = web.input()
        mobile = params.mobile
        poid = int(params.poid)

        siteuser = cms_model.SiteUser(passwd='abcd1234',mobile=mobile)
        siteuser.email=''
        # siteuser.up.address = params.address
        # siteuser.up.birthday = params.birthday

        try:
            uid = cmsService.create_siteuser(siteuser)
            cmsService.update_porder_status(poid,uid,2)
            return '{"status":"OK"}'
        except BaseException,e:
            return e

#TODO this needs to be optimized
class CreateSiteUserHandler():
    def GET(self):
        return render.siteuser_form(None)


    def POST(self):
        params = web.input()
        mobile = params.mobile
        siteuser = cms_model.SiteUser(passwd='abcd1234',mobile=mobile,email=params.email,nickname=params.nickname)
        siteuser.up.address = params.address
        siteuser.up.birthday = params.birthday
        siteuser.up.remark = params.remark

        try:
            uid = cmsService.create_siteuser(siteuser)
            return '{"status":"OK"}'
        except BaseException,e:
            return e


class SiteUserList():
    def GET(self):
        try:
            params = web.input(uid=None)
            uid = None
            if params.uid:
                uid = int(params.uid)

            rlist = cmsService.list_siteuser(uid)
            return render.siteuser_list(rlist)
        except BaseException,e:
            return e


class GetSiteUser():
    def GET(self,uid):
        user = cmsService.get_siteuser(int(uid))
        return render.siteuser_form(user)

class DeleteSiteUser():
    def GET(self,uid):
        cmsService.delete_siteuser(int(uid))
        return web.seeother('/siteuser/list')

#TODO
class ResetSiteUserPassword():
    def GET(self,uid):
        return ""

    def POST(self,uid):
        cmsService.delete_siteuser(int(uid))
        return web.seeother('/siteuser/list')


class SaveSiteUser():
    def POST(self):
        # try:
        params = web.input()

        cmsService.save_siteuser(**{'uid':int(params.id),'email':params.email,'nickname':params.nickname,'mobile':params.mobile,'status':int(params.status)
            ,'address':params.address,'birthday':params.birthday,'remark':params.remark})

        return render.common('Saved OK:%s' %params.id)
        # except BaseException ,e:
            #return e


class DownloadSelectedImageResult():
    def GET(self,oid):
        try:
            rlist = cmsService.list_selected_imgs(int(oid))
            selected_filenames=[]
            for i in range(0,len(rlist)):
               img=rlist[i]
               img_filename = img.file.split('/')[-1]
               selected_filenames.append(img_filename)

            selected_content = " ".join(selected_filenames)

            #set http response header here
            web.header("content-disposition", 'attachment; filename="' + 'simglist_'+str(oid)+'"')
            web.header("content-length",str(len(selected_content)))
            return selected_content

        except BaseException,e:
            return e

class ChangeOrderStatus():
    def GET(self):
        params = web.input()
        oid = int(params.oid)
        order_id = int(oid)
        order = cmsService.load_order(order_id)
        return render.order_form_status(order)

    def POST(self):
        params = web.input()
        oid = int(params.oid)
        status = int(params.status)

        result = cmsService.update_order_status(oid,status)

        if result:
            return web.seeother('/orders')
        else:
            return render.common("Failed")


class GetOrderImageCover():
    def GET(self,oid):
        img = cmsService.get_order_imgcover(oid)
        if img:
            return img.file
        else:
            return ""


class TotalCounterHandler():
    def GET(self):
        params = web.input()
        msg_type = params.msg_type

        counter = 0
        if 'user' == msg_type:
            counter = cmsService.get_total_siteuser()

        elif 'order' == msg_type:
            counter = cmsService.get_total_order()



