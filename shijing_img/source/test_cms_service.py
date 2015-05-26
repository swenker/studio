__author__ = 'wenju'

from cms import cms_service
from cms.cms_model import *
from cms import aliyun_oss_handler

cmsService = cms_service.cmsService


def test_get_article_content(id):
    return cmsService.get_article_content(id)


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
        article = ArticleEntity(article_meta, article_content)

        cmsService.new_article(article)


    def test_list_articles(self):
        return cmsService.list_articles(0, 10)


    def test_get_article(self, id):
        return cmsService.get_article(id)


    def test_get_article_meta(self, id):
        return cmsService.get_article_meta(id)


    def test_get_article_content(self, id):
        return cmsService.get_article_content(id)


    def test_save_album(self):
        album = Album()
        album.title = "Default"
        cmsService.save_album(album)

        album = Album()
        album.title = "Private"
        cmsService.save_album(album)


    def test_create_img(self):
        imglist = []
        imglist.append(Image(title="sunset", aid=1, file="/2014/12/28/img.jpg"))
        imglist.append(Image(title="Tree", aid=1, file="/2014/12/21/img.jpg"))
        imglist.append(Image(title="Portrait", aid=1, file="/2014/12/25/img.jpg"))
        imglist.append(Image(title="Cloud ", aid=1, file="/2014/12/29/img.jpg"))

        cmsService.create_img(Image(title="Cloud ", aid=1, file="/2014/12/18/img.jpg"))


    def test_get_album_list(self):
        return cmsService.get_album_list()


    def test_get_album_imglist(self):
        return cmsService.get_album_imglist('ac')


    def test_article_write(self):
        self.test_new_article()


    def test_article_get(self):
        print self.test_list_articles()
        print self.test_get_article(1)

        print self.test_get_article_meta(1)
        print test_get_article_content(tcs.test_get_article_meta(1).cid)
        print test_get_article_content(5)


    def test_album_write(self):
        self.test_save_album()
        self.test_create_img()


    def test_album_get(self):
        print self.test_get_album_list()
        print self.test_get_album_imglist()

    def test_list_category(self):
        print cmsService.get_category_list()

    def test_time_conversion(self):
        aliyun_oss_handler.upload_file_to_oss(None,None)

    def test_batch_image(self):
        folder = '/2015/05/26'
        aid =100
        orderid = 2015
        from cms import batch_image_handler
        batch_image_handler.load_local_folder(aid,folder,orderid)


def abc():
    print "abc"

if __name__ == '__main__':
    tcs = TestCmsService()
    # tcs.test_article_get()
    #tcs.test_album_get()

    # tcs.test_article_write()
    # tcs.test_album_write()
    # tcs.test_list_category()

    # tcs.test_time_conversion()

    tcs.test_batch_image()


