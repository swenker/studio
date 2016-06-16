__author__ = 'wenju'

import os,sys
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from cms import cms_service
from cms.cms_model import *
from cms import aliyun_oss_handler

cmsService = cms_service.cmsService



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

        article_id = cmsService.new_article(article)
        self.assertTrue(article_id)

        cmsService.delete_article(article_id,True)

        self.assertFalse(cmsService.get_article(article_id))

    #TODO add more cases,such as by code and so on
    def test_list_articles(self):
        self.assertEqual(2,len(cmsService.list_articles(0, 2)))


    def test_get_article(self):
        article_id = 1
        self.assertEqual(article_id,cmsService.get_article(article_id).article_meta.oid)


    def test_get_article_meta(self):
        article_id = 1
        self.assertEqual(article_id,cmsService.get_article_meta(article_id).oid)


    def test_get_article_content(self):
        article_content_id = 1
        self.assertEqual(article_content_id,cmsService.get_article_content(article_content_id).oid)


    # def test_save_album(self):
    #     album = Album()
    #     album.title = "Default"
    #     cmsService.save_album(album)
    #
    #     album = Album()
    #     album.title = "Private"
    #     cmsService.save_album(album)
    #
    #
    # def test_create_img(self):
    #     imglist = []
    #     imglist.append(Image(title="sunset", aid=1, file="/2014/12/28/img.jpg"))
    #     imglist.append(Image(title="Tree", aid=1, file="/2014/12/21/img.jpg"))
    #     imglist.append(Image(title="Portrait", aid=1, file="/2014/12/25/img.jpg"))
    #     imglist.append(Image(title="Cloud ", aid=1, file="/2014/12/29/img.jpg"))
    #
    #     cmsService.create_img(Image(title="Cloud ", aid=1, file="/2014/12/18/img.jpg"))


    def test_get_album_list(self):
        self.assertEqual(4,len(cmsService.get_album_list()))


    def test_get_album_imglist(self):
        return cmsService.get_album_imglist('ac')


    def test_list_category(self):
        self.assertEqual(5,len(cmsService.get_category_list()))


    # def test_time_conversion(self):
    #     aliyun_oss_handler.upload_file_to_oss(None,None)

    def test_batch_load_imagefolder(self):
        folder = '/2015/05/26'
        aid =100
        orderid = 2015
        from cms import batch_image_handler
        batch_image_handler.load_local_folder(aid,folder,orderid)
        cmsService.delete_order_img(2015)

    # def test_delete_preorder(self):
    #      cmsService.delete_preorder(2)

    def test_save_order(self):
        order = Order(1)
        order.title = "test title"
        order.edit_limit= 40
        order.total_limit = 120
        order.price=999.00
        order.remark = 'remark'
        order.venue = 'venue'
        order.dttake = '2015-08-22'

        cmsService.save_order(order)

        self.assertTrue(order.oid)

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

        #remove the test data
        cmsService.delete_siteuser(uid)
        self.assertFalse(cmsService.get_siteuser(uid))


    def test_list_siteuser(self):
        siteuser_list = cmsService.list_siteuser()
        # print siteuser_list
        self.assertTrue(len(siteuser_list)>1)

    #TODO more cases go here.

    def test_delete_order_img(self):
        cmsService.delete_order_img(2015)

    def test_get_agenda(self):
        cmsService.get_agenda('')

    def test_create_preorder(self):

        po = Preorder()
        po.age = 3
        po.bdesc = "Baby girl"
        po.genre = 0
        po.mobile = '18601203570'
        po.pdate = '2016-08-13'
        po.utitle = "Alice"
        po.status = 1

        mid = cmsService.create_preorder(po)
        self.assertTrue(mid)

        cmsService.delete_preorder(mid)


    def test_list_preorder_all(self):
        polist = cmsService.list_preorder(None,None)

        self.assertEqual(len(polist),3)

        polist = cmsService.list_preorder(1,None)

        self.assertEqual(len(polist),3)

    def test_list_preorder_by_status(self):
        polist = cmsService.list_preorder(None,1)

        self.assertEqual(len(polist),2)

        print polist

    def test_list_preorder(self):
        polist = cmsService.list_preorder(1,2)

        self.assertEqual(len(polist),1)

        polist = cmsService.list_preorder(2,status=None,pdate='2016-08')

        self.assertEqual(len(polist),1)


    def test_list_orders_byuser(self):
        uid = 110
        print len(cmsService.list_orders(uid))



if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(CmsServiceTestCase)
    suite = unittest.TestSuite()
    tests = ['test_batch_load_imagefolder']
    tests = ['test_delete_order_img']
    tests = ['test_batch_load_imagefolder']

    tests = ['test_create_preorder']
    tests = ['test_list_preorder_all','test_list_preorder_by_status','test_list_preorder']
    tests = ['test_list_preorder']

    tests = ['test_list_orders_byuser']
    for test in tests:
        suite.addTest(CmsServiceTestCase(test))

    unittest.TextTestRunner(verbosity=2).run(suite)




