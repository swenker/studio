__author__ = 'wenju'

import os,sys
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from cms import cms_service
from cms.cms_model import *
from cms import aliyun_oss_handler

cmsService = cms_service.cmsService


def test_get_article_content(id):
    return cmsService.get_article_content(id)


class CmsServiceTestCase(unittest.TestCase):
    def setUp(self):
        # print "Test Cms Service"
        pass

    def tearDown(self):
        # print "End of Test.."
        pass

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

    def test_delete_preorder(self):
         cmsService.delete_preorder(2)

    def test_save_order(self):
        order = Order(1)
        order.title = "test title"
        order.edit_limit= 40
        order.total_limit = 120
        order.price=999.00
        order.remark = 'remark'
        order.venue = 'venue'
        order.dttake = '2015-08-22'

        print cmsService.save_order(order)

        tmp_order = cmsService.load_order(order.oid)
        self.assertEqual(tmp_order.edit_limit,40)

        cmsService.delete_order(order.oid)
        self.assertFalse(cmsService.load_order(order.oid))

    def test_list_order(self):
        self.assertTrue(len(cmsService.list_orders())>0)


    def test_save_siteuser(self):
         params = {'uid':'1','email':'abc@abc.com','nickname':'Katy','mobile':'1860120','status':'1','address':'Wangjing','birthday':'2010-09-13','remark':'I am test'}
         cmsService.save_siteuser(**params)

         site_user = cmsService.get_siteuser(1)
         self.assertEquals(site_user.email,'abc@abc.com')
         print site_user


    def test_create_siteuser(self):
        site_user = SiteUser()
        site_user.email = 'swenker01@gmail.com'
        site_user.mobile = '18912345678'
        site_user.nickname = 'Welbo'
        site_user.passwd = 'abcd1234'

        site_user.up = SiteUserProfile()
        site_user.up.address = 'Wangjing Road'
        site_user.up.birthday = '2010-01-01'
        site_user.up.remark = 'I am test'

        uid = cmsService.create_siteuser(site_user)

        self.assertTrue(uid > 1)

        cmsService.delete_siteuser(uid)

        self.assertFalse(cmsService.get_siteuser(uid))


    def test_list_siteuser(self):
        siteuser_list = cmsService.list_siteuser()
        # print siteuser_list
        self.assertTrue(len(siteuser_list)>1)


if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(CmsServiceTestCase)
    suite = unittest.TestSuite()
    tests = ['test_list_siteuser','test_list_order']
    for test in tests:
        suite.addTest(CmsServiceTestCase(test))

    unittest.TextTestRunner(verbosity=2).run(suite)




