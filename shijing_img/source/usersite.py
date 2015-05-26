__author__ = 'wenjusun'

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
import wshelper


urls = (
        "/login", "LoginService",
        "", "LoginService",
        "/orders", "ListOrders",
        "/listimgs/(\d+)", "ListOrderImages",
        "/okimgs/(\d+)", "ListSelectedImages",
        "/upc/(\d+)", "UpdateChoice",
        "/order/(\d+)", "GetOrder",
        "/user/(\d+)", "GetUser"
)

app = web.application(urls, globals())
config = service_config.config

t_globals = {
    'datestr': web.datestr,
    'service_config':config
}

render = web.template.render("templates/user", globals=t_globals)

cmsService = cms_service.CmsService()

serviceHelper = wshelper.ServiceHelper()

class Dashboard():
    def GET(self):
        return render.dashboard()


class LoginService():
    def GET(self):
        return render.login('')

    def POST(self):
        params = web.input()
        email = params.email
        passwd = params.passwd

        #print "abc:"+email,passw
        if email and passwd:
            stat,reason = cmsService.site_user_login(email,passwd)
            if(reason=='OK'):
                return web.seeother('/dashboard')
            else:
                return render.login("Failed:"+reason)
        else:
            return render.login("Please Input email and password")


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
        rlist = cmsService.list_order_imgs(int(oid))

        return render.img_list_select(rlist, len(rlist))

class ListSelectedImages():
    def GET(self,oid):
        rlist = cmsService.list_selected_imgs(int(oid))

        return render.img_select_result(rlist, len(rlist))


