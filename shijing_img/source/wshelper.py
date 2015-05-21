__author__ = 'sunwj'

import os

from datetime import datetime
from cms.aliyun_oss_handler import *
from cms import cms_model
from cms import service_config
from cms.image_processor import ImageProcessor
import httplib

config = service_config.config

logger = config.getlogger("CmsService")
improcessor = ImageProcessor()

class ServiceHelper():
    def load_config(self):
        pass

    def preview(self):
        pass

    def save(self, params):
        pass

    def publish(self):
        pass

    def store(self, image):

        base_store_path = config.img_save_path
        imgpath = image.file.filename.replace('\\', '\\')
        imgname = imgpath.split('/')[-1]

        date_path = datetime.now().strftime("%Y/%m/%d")

        # relative_store_dir = "raw/%s" % date_path
        relative_dir = "/%s" % date_path

        raw_relative_dir="raw/"+date_path
        large_relative_dir="lar/"+date_path
        thumb_relative_dir="thumb/"+date_path

        raw_full_store_dir = "%s/%s" % (base_store_path, raw_relative_dir)
        large_full_store_dir = "%s/%s" % (base_store_path, large_relative_dir)
        thumb_full_store_dir = "%s/%s" % (base_store_path, thumb_relative_dir)

        if not os.path.exists(raw_full_store_dir):
            os.makedirs(raw_full_store_dir)

        if not os.path.exists(large_full_store_dir):
            os.makedirs(large_full_store_dir)

        if not os.path.exists(thumb_full_store_dir):
            os.makedirs(thumb_full_store_dir)

        local_tmp_path_pattern = "%s/%s"


        fout = open((local_tmp_path_pattern%(raw_full_store_dir,imgname)), 'w')
        fout.write(image.file.file.read())
        fout.close()

        improcessor.thumbnail(date_path)
        improcessor.large(date_path)



        img_store = config.img_store
        if img_store == 'oss':
            upload_file_to_oss(raw_relative_dir+"/"+imgname,(local_tmp_path_pattern%(raw_full_store_dir,imgname)))
            upload_file_to_oss(large_relative_dir+"/"+imgname,(local_tmp_path_pattern%(large_full_store_dir,imgname)))
            upload_file_to_oss(thumb_relative_dir+"/"+imgname,(local_tmp_path_pattern%(thumb_full_store_dir,imgname)))

        return imgname,relative_dir + "/" + imgname


    def generateIndexHtml(self):
        httpcon = httplib.HTTPConnection("localhost")
        httpcon.connect()
        httpcon.request("GET","/p/site/home")
        httpresp=httpcon.getresponse()

        if httpresp.status==200:
            out_html = config.web_base+"/index.html"
            fout = open(out_html, 'w')
            fout.write(httpresp.read())
            fout.close()
            logger.info("generated.")
        else:
            logger.error("Failed to generate html :%d %s" %(httpresp.status,httpresp.reason))
        httpcon.close()


    def compose_article(self, params):
        article_meta = cms_model.ArticleMeta()

        if params.oid:
            article_meta.oid = int(params.oid)
        else:
            article_meta.oid = -1

        article_meta.title = params.title

        article_meta.subtitle = params.subtitle
        article_meta.author = params.author
        article_meta.source = params.source
        article_meta.cover = params.cover
        article_meta.ctcode = params.ctcode[0]

        # article_meta.dtpub = datetime.now().strftime(TIME_FORMAT)
        #todo auto generate
        article_meta.brief = 'This is brief'
        article_meta.status = 1

        article_content = cms_model.ArticleContent(params.content)

        if params.cid:
            article_content.oid = int(params.cid)

        article = cms_model.ArticleEntity(article_meta, article_content)

        return article

    def compose_category(self,params):
        category = cms_model.Category()

        if params.oid:
            category.oid = params.oid

        category.title = params.title
        category.code = params.code
        category.remark = params.remark
        category.status = params.status

        return category



