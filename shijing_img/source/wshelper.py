__author__ = 'sunwj'

import os

from datetime import datetime
from cms.aliyun_oss_handler import *

from cms import cms_model


class ServiceHelper():
    def load_config(self):
        pass

    def preview(self):
        pass

    def save(self, params):
        pass

    def publish(self):
        pass

    def store(self, image, base_store_path):
        # TODO genreate thumbnail and upload all of them to to oss(/)

        imgpath = image.file.filename.replace('\\', '\\')
        imgname = imgpath.split('/')[-1]

        date_path = datetime.now().strftime("%Y/%m/%d")
        relative_store_dir = "raw/%s" % date_path
        relative_dir = "/%s" % date_path
        full_store_dir = "%s/%s" % (base_store_path, relative_store_dir)

        if not os.path.exists(full_store_dir):
            os.makedirs(full_store_dir)

        local_tmp_path = full_store_dir + "/" + imgname
        fout = open(local_tmp_path, 'w')
        fout.write(image.file.file.read())
        fout.close()

        #160*...

        #320*..

        #raw
        upload_file_to_oss(relative_store_dir+"/"+imgname,local_tmp_path)

        return imgname,relative_dir + "/" + imgname


    def compose_article(self, params):
        article_meta = cms_model.ArticleMeta()

        if params.id:
            article_meta.id = int(params.id)
        else:
            article_meta.id = -1

        article_meta.title = params.title

        article_meta.subtitle = params.subtitle
        article_meta.author = params.author
        article_meta.source = params.source
        # article_meta.dtpub = datetime.now().strftime(TIME_FORMAT)
        #todo auto generate
        article_meta.brief = 'This is brief'
        article_meta.status = 1

        article_content = cms_model.ArticleContent(params.content)

        if params.cid:
            article_content.id = int(params.cid)

        article = cms_model.ArticleEntity(article_meta, article_content)

        return article

