__author__ = 'wenjusun'

import web
import admcms
import wndxsite
import usersite
from cms import batch_image_handler

urls = ("/p/site", wndxsite.app,
        "/p/adm", admcms.app,
        "/p/u", usersite.app
)

job_service = batch_image_handler.JobService()
job_service.start_worker_thread()

app = web.application(urls, globals())
application=app.wsgifunc()
