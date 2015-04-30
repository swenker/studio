__author__ = 'wenjusun'


import cgi
import web

urls = ("/p/hello","HelloWeb")

app = web.application(urls, globals())
application = app.wsgifunc()

class HelloWorld():
    def GET(self):
        return "HelloPython"
