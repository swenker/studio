__author__ = 'wenjusun'

import web
import admcms
import wndxsite


urls = ("/p/site", wndxsite.app,
        "/p/adm", admcms.app
)

app = web.application(urls, globals())
application=app.wsgifunc()