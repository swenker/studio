__author__ = 'wenjusun'

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
import wshelper
from cms import batch_image_handler

urls = (
        "/login", "LoginService",
        "/logout", "LogoutService",
        "", "LoginService",
        "/orders", "ListOrders",
        "/listimgs/(\d+)", "ListOrderImages",
        "/okimgs/(\d+)", "ListSelectedImages",
        "/upc/(\d+)", "UpdateChoice",
        "/order/(\d+)", "GetOrder",
        "/user/(\d+)", "GetUser",
        "/loadfolder","LoadFolder"
)

app = web.application(urls, globals())
web.config.debug=False

#web.config.session_parameters['timeout'] = 8000
# web.config.session_parameters['ignore_change_ip'] = True
print '---------------------------------------------------------------------------------------------------------------'
session = web.session.Session(app, web.session.DiskStore('sessions/site_users'), initializer={'uinfo': None})

config = service_config.config

t_globals = {
    'datestr': web.datestr,
    'service_config':config
}

render = web.template.render("templates/user", globals=t_globals)

cmsService = cms_service.cmsService

serviceHelper = wshelper.ServiceHelper()

class Dashboard():
    def GET(self):
        return render.dashboard()

class UserInfo():
    def __init__(self,user,order):
        self.user = user
        self.order = order

class LoginService():
    def GET(self):
        #userinfo=serviceHelper.get_user_session(web,app)
        userinfo = session.uinfo
        if not userinfo:
            return render.login('')
        else:
            return web.seeother('/listimgs/'+str(userinfo.order.oid))

    def POST(self):
        params = web.input()
        # email = params.email
        mobile = params.mobile
        passwd = params.passwd

        #print "abc:"+email,passw
        if mobile and passwd:
            stat,reason = cmsService.site_user_login(mobile,passwd)
            if(reason=='OK'):
                user = stat
                orders = cmsService.list_orders(user.oid)
                session.uinfo =UserInfo(user,None)
                if orders:
                    order = orders[0]

                    #serviceHelper.save_user_session(web,app,UserInfo(user,order))
                    session.uinfo = UserInfo(user,order)

                    return web.seeother('/listimgs/'+str(order.oid))
                else:
                    return web.seeother('/home')
            else:
                return render.login("Failed:"+reason)
        else:
            return render.login("Please Input email and password")

class LogoutService():
    def GET(self):
        print session
        #serviceHelper.delete_user_session(web,app)
        session.kill()
        return web.seeother('/login')


class GetUser():
    def GET(self,uid):
        pass

class GetOrder():
    def GET(self,oid):
        pass


class UpdateChoice():
    def GET(self, iid):
        params = web.input()
        # oid = int(params.oid)
        status = int(params.status)
        # cmsService.update_user_choice(iid,oid,status)
        cmsService.update_user_choice(iid,status)
        return "{'result':'OK'}"

class ListOrders():
    def GET(self):
        params = web.input(uid=None)

        uid = None
        if params.uid:
            uid = int(params.uid)

        rlist, total = cmsService.list_orders(uid)

        return render.order_list(rlist, total)



class ListOrderImages():
    "List all images of for the order"
    def GET(self,oid):

        userinfo=serviceHelper.get_user_session(session)

        if userinfo:
            rlist = cmsService.list_order_imgs(int(oid))
            return render.img_list_select(userinfo.order,rlist, len(rlist))
        else:
            return render.common("<a href='/p/u/login'>please login</a>")

class ListSelectedImages():
    def GET(self,oid):
        rlist = cmsService.list_selected_imgs(int(oid))

        return render.img_select_result(rlist, len(rlist))



class LoadFolder():
    def GET(self):

        return render.load_folder()

    def POST(self):
        params = web.input()
        folder = params.folder

        orderid = int(params.orderid)

        batch_image_handler.load_local_folder(cms_service.album_map.get('oa').oid,folder,orderid)

        web.seeother('/listimgs/'+str(orderid))
