__author__ = 'samsung'

import web
import model

urls = ('/c/list','List',
        '/c/show/(\d+\.\d+\.\d+\.\d+)','Detail',
        '/c/report',"Report"
)


class List():
    def GET(self):

        configlist=model.getconfiglist()
        #This tells web.py to look for templates in your templates directory.
        render=web.template.render("templates/")
        return render.list(configlist)


class Detail():
    #lip should be corresponding to the part in () after /
    def GET(self,lip):
        self.getconfigbylip(lip)

    def getconfigbylip(self,lip):
        return model.getconfigbylip(lip)


class Report():
    def POST(self):
        params=web.input(wip=None)
        conf=model.Config(params.lip,int(params.totalmem),int(params.cpu),params.wip)
        #print conf
        model.saveconfig(conf)
        return "OK"


app=web.application(urls,globals())
application = app.wsgifunc()

if __name__=="__main__":
    app.run()
