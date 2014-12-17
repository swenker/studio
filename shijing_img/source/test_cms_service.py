__author__ = 'samsung'


from datetime import datetime
from cms.cms_service import *
from cms.cms_model import *
from cms.service_config import *


cmsService = CmsService()

class TestCmsService():
    def test_new_article(self):
        article_meta = ArticleMeta()
        article_meta.id = -1
        article_meta.title = 'this is title'
        article_meta.subtitle = 'subtitle'
        article_meta.cover = 'cover'
        article_meta.author = 'author'
        article_meta.source = 'source'
        article_meta.dtpub = datetime.now().strftime(TIME_FORMAT)
        article_meta.dtupdate = ''
        article_meta.brief = 'This is brief'
        article_meta.status = 2

        article_content = ArticleContent("This content")
        article = ArticleEntity(article_meta,article_content)

        cmsService.new_article(article)

    def test_list_articles(self):
        return cmsService.list_articles(0,10)

    def test_get_article(self,id):
        return cmsService.get_article(id)

    def test_get_article_meta(self,id):
        return cmsService.get_article_meta(id)

    def test_get_article_content(self,id):
        return cmsService.get_article_content(id)


    def test_save_album(self):
        album = Album()
        album.title="Default"
        cmsService.save_album(album)

        album = Album()
        album.title="Private"
        cmsService.save_album(album)

    def test_create_img(self):

        imglist=[]
        imglist.append(Image(title="sunset",aid=1,file="/2014/12/28/img.jpg"))
        imglist.append(Image(title="Tree",aid=1,file="/2014/12/21/img.jpg"))
        imglist.append(Image(title="Portrait",aid=1,file="/2014/12/25/img.jpg"))
        imglist.append(Image(title="Cloud ",aid=1,file="/2014/12/29/img.jpg"))

        cmsService.create_img(imglist)

    def test_get_album_list(self):
        print cmsService.get_album_list()

    def test_get_album_imglist(self):
        print cmsService.get_album_imglist(1)


    def test_article_operation(self):
        #print tcs.test_list_articles()

        #print tcs.test_get_article(1)
        self.test_new_article()
        print self.test_get_article_meta(1)
        print self.test_get_article_content(tcs.test_get_article_meta(1).cid)
        print self.test_get_article_content(5)


    def test_album_operation(self):
        # self.test_save_album()
        # self.test_create_img()
        self.test_get_album_list()
        self.test_get_album_imglist()

if __name__ == '__main__':
    tcs = TestCmsService()
    tcs.test_album_operation()


