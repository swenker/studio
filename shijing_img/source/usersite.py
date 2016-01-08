__author__ = 'wenjusun'

import cgi
import web

from cms import cms_model
from cms import cms_service
from cms import service_config
from cms import cms_utils

import wshelper

urls = (
    "/login", "LoginService",
    "/logout", "LogoutService",
    "", "LoginService",
    "/orders", "ListOrders",
    "/listimgs/(\d+)", "ListOrderImages",
    "/okimgs/(\d+)", "ListSelectedImages",
    "/upc/(\d+)", "UpdateChoice",
    "/order/(\d+)", "GetOrder",
    "/order/confirm_select/(\d+)", "ConfirmOrderImageSelection",
    "/order/imgcover/(\d+)","GetOrderImageCover",
    "/user/(\d+)", "GetUser"
)

app = web.application(urls, globals())
web.config.debug = False

# web.config.session_parameters['timeout'] = 8000
# web.config.session_parameters['ignore_change_ip'] = True
print '---------------------------------------------------------------------------------------------------------------'

config = service_config.config

t_globals = {
    'daystr': cms_utils.daystr,
    'service_config': config
}

render = web.template.render("templates/user", globals=t_globals)

cmsService = cms_service.cmsService

serviceHelper = wshelper.ServiceHelper()
session = serviceHelper.init_user_session(web, app)

logger = config.getlogger()
logger.info('usersite initialized')


def my_loadhook():
    request_uri = web.ctx.environ.get('REQUEST_URI')
    if not session.get('uinfo') and request_uri != '/p/u/login':
        web.seeother('/login')


app.add_processor(web.loadhook(my_loadhook))


class Dashboard():
    def GET(self):
        return render.dashboard()


class UserInfo():
    def __init__(self, user):
        self.user = user
        self.order = None
        self.order_idlist = None

    def is_order_owner(self, oid):
        #logger.info(("=========%d====================&s========", oid, self.order_idlist))
        if self.order_idlist:
            return self.order_idlist.count(oid) == 1


class LoginService():
    def GET(self):
        userinfo = serviceHelper.get_user_session(session)
        if not userinfo:
            return render.login('')
        else:
            return web.seeother('/listimgs/' + str(userinfo.order.oid))

    def POST(self):
        params = web.input()
        # email = params.email
        mobile = params.mobile
        passwd = params.passwd

        if mobile and passwd:
            stat, reason = cmsService.site_user_login(mobile, passwd)
            if (reason == 'OK'):
                user = stat
                # orders = cmsService.list_orders_bystatus(cms_model.Order.ORDER_SELECTING, user.oid)
                orders = cmsService.list_orders(user.oid)

                session.uinfo = UserInfo(user)
                selecting_order=None
                if orders:
                    order_idlist = []
                    for od in orders:
                        order_idlist.append(od.oid)
                        if od.status == cms_model.Order.ORDER_SELECTING:
                            selecting_order=od
                    session.uinfo.order_idlist = order_idlist
                    session.uinfo.order = selecting_order

                    return web.seeother('/listimgs/' + str(session.uinfo.order.oid))
                else:
                    return web.seeother('/orders')
            else:
                return render.login("Failed:" + reason)
        else:
            return render.login("Please Input email and password")


class LogoutService():
    def GET(self):
        #serviceHelper.delete_user_session(web,app)
        session.kill()
        return web.seeother('/login')


class GetUser():
    def GET(self, uid):
        pass


class GetOrder():
    def GET(self, oid):
        pass


class UpdateChoice():
    def GET(self, iid):
        params = web.input()
        # oid = int(params.oid)
        status = int(params.status)
        # cmsService.update_user_choice(iid,oid,status)
        cmsService.update_user_choice(iid, status)
        return "{'result':'OK'}"


class ListOrders():
    def GET(self):
        userinfo = serviceHelper.get_user_session(session)
        uid = userinfo.user.oid

        rlist = cmsService.list_orders(uid)

        return render.order_list(rlist, len(rlist))


class ListOrderImages():
    "List all images of for the order"

    def GET(self, oid):
        userinfo = serviceHelper.get_user_session(session)
        i_oid = int(oid)
        if userinfo:
            if userinfo.is_order_owner(i_oid):
                rlist = cmsService.list_order_imgs(i_oid)
                return render.img_list_select(oid, rlist, len(rlist))
            else:
                return render.common("Invalid request")
        else:
            return render.common("<a href='/p/u/login'>please login</a>")


class ListSelectedImages():
    def GET(self, oid):
        userinfo = serviceHelper.get_user_session(session)
        i_oid = int(oid)
        if userinfo:
            if userinfo.is_order_owner(i_oid):
                rlist = cmsService.list_selected_imgs(i_oid)
                return render.img_select_result(oid, rlist, len(rlist))
            else:
                return render.common("Invalid request")
        else:
            return render.common("<a href='/p/u/login'>please login</a>")


class GetOrderImageCover():
    def GET(self,oid):
        img = cmsService.get_order_imgcover(oid)
        if img:
            return img.file
        else:
            return ""


class ConfirmOrderImageSelection():
    def GET(self, oid):
        cmsService.update_order_status(int(oid), cms_model.Order.ORDER_SELECTED)

        return web.seeother('/orders')


class GetUserInfo():
    def GET(self):
        userinfo = serviceHelper.get_user_session(session)
        if userinfo:
            return "{'user':'"+userinfo.mobilef+"'}"