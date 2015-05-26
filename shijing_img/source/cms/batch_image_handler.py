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

    def scan(self,relative_path):
        full_path = config.img_save_path+"/raw"
        files = glob.glob(full_path+"/*.jpg")
        filenames=[]
        if files:
            for f in files:
                filenames.append(f.split('/')[-1])

        return filenames


class RecordStore():
    def __init__(self):
        self.fileScanner = LocalFileScanner()
        self.imageProcessor = ImageProcessor()

    def process(self,aid,relative_path):
        filenames = self.fileScanner.scan(relative_path)

        #save
        for f in filenames:
            cmsService.create_img(self.compose_image(relative_path,f))

        #zoom
        self.imageProcessor.thumbnail(relative_path)
        self.imageProcessor.medium(relative_path)
        self.imageProcessor.large(relative_path)

        logger.info('done for:'+relative_path)


    def compose_image(self,relative_path,title):
        image = Image(title)

        image.file =  relative_path+'/'+filename

        image.itype=Image.IMG_TYPE_USER

        return image

