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



if __name__ == '__main__':
    tcs = TestCmsService()
    tcs.test_new_article()
    #print tcs.test_list_articles()

    #print tcs.test_get_article(1)
    print tcs.test_get_article_meta(1)
    print tcs.test_get_article_content(tcs.test_get_article_meta(1).cid)
    print tcs.test_get_article_content(5)


