__author__ = 'sunwj'

import web


urls=("/cps/adminsvc","NewMessage",
      "/cps/newa","NewArticle")
web.config.debug = False
app=web.application(urls,globals())
application = app.wsgifunc()

#session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates")

class NewArticle():
    def GET(self):
        return "new_article.html"
    def POST(self):

        return render.common("OK")


class NewArticleHelper():
    def preview(self):

#It can not be run on Windows
if __name__=="__main__":
    app.run()
