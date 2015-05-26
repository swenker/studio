__author__ = 'wenjusun'

import glob
from service_config import config
import cms_service
from cms_model import *
from image_processor import ImageProcessor

"""
    to deal with those images batch uploaded?
    the images will be manually uploaded to a folder /raw/.....
"""

cmsService = cms_service.CmsService()
logger = config.getlogger('batch_process')


class LocalFileScanner():
    def __init__(self):
        pass

    def scan(self,relative_folder):
        full_path = config.img_save_path+"/raw"+relative_folder
        # files = glob.glob(full_path+"/*.jpg")
        files = glob.glob(full_path+"/*")
        filenames=[]
        if files:
            for f in files:
                filenames.append(f.split('/')[-1])

        return filenames


class RecordStore():
    def __init__(self,fileScanner):
        self.fileScanner = fileScanner
        self.imageProcessor = ImageProcessor()

    def process(self,aid,relative_folder,orderid):
        filenames = self.fileScanner.scan(relative_folder)

        logger.info('total files:%d' % len(filenames))

        #save
        counter = 0
        for f in filenames:
            iid = cmsService.create_img(self.compose_image(relative_folder,f,aid))
            cmsService.add_order_img(iid,orderid)

            #zoom
            relative_folder_file = relative_folder + '/' + f
            self.imageProcessor.thumbnail(relative_folder_file)
            self.imageProcessor.medium(relative_folder_file)
            self.imageProcessor.large(relative_folder_file)

            counter += 1
        logger.info('done for(%s,%d):'%(relative_folder,counter))


    def compose_image(self, relative_path, title,aid):
        image = Image(title=title)

        image.file =  relative_path + '/' + title
        image.aid = aid
        image.itype = Image.IMG_TYPE_USER

        return image


def load_local_folder(aid,relative_folder,orderid):
    recordStore = RecordStore(LocalFileScanner())
    recordStore.process(aid,relative_folder,orderid)