__author__ = 'wenjusun'

import web
import admcms
import wndxsite
import usersite


urls = ("/p/site", wndxsite.app,
        "/p/adm", admcms.app,
        "/p/u", usersite.app
)

app = web.application(urls, globals())
application=app.wsgifunc()