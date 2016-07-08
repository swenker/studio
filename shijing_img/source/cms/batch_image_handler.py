__author__ = 'wenjusun'

import threading
import time
import Queue
import glob
from service_config import config
import cms_service
from cms_model import *
from aliyun_oss_handler import *
from image_processor import ImageProcessor

"""
    to deal with those images batch uploaded?
    the images will be manually uploaded to a folder /raw/.....
"""

cmsService = cms_service.cmsService
logger = config.getlogger('batch_image_handler')


completed_tasks={}


class PhotoJob():
    def __init__(self,order_id,relative_folder,album_id):
        self.album_id = album_id
        self.order_id = order_id
        self.relative_folder = relative_folder

    def __str__(self):
        return "PhotoJob:albumId[%d],orderId[%d],relative_folder[%s]" % (self.album_id,self.order_id,self.relative_folder)

def submit_job(job,job_queue):
    job_queue.put(job)
    logger.info("%d Enqueue new Job: JobID:%d,queue size:%d" %(id(job_queue),job.order_id,job_queue.qsize()))

def handle_photos(job_queue):
    while True:
        if not job_queue.empty():
            job = job_queue.get_nowait()
            logger.info("------------got job:%d" %job.order_id)

            counter = 1
            # counter = load_local_folder(job.album_id,job.relative_folder,job.order_id)
            print "=============================================I am a task========================="
            completed_tasks[job.order_id]='{"OK":%d}' %counter
            job_queue.task_done()
        else:
            logger.info("the queue is empty. will sleep 1 minute:%d..." %(job_queue.qsize()))
            time.sleep(20)

def start_worker_thread(job_queue):
    worker_thread = threading.Thread(target=handle_photos,args=(job_queue,))
    worker_thread.setDaemon(True)
    worker_thread.start()

class OrderPhotoProcessor(threading.Thread):

    def __init__(self,job_queue):
        super(OrderPhotoProcessor,self).__init__()
        self.job_queue = job_queue

    def run(self):
        while True:
            # logger.debug(self.job_queue.qsize())

            if not self.job_queue.empty():
                logger.info("-------------------will get job from queue......")
                job = self.job_queue.get_nowait()
                logger.info("------------got job:%d" %job.order_id)

                counter = 1
                # counter = load_local_folder(job.album_id,job.relative_folder,job.order_id)
                print "=============================================I am a task========================="
                completed_tasks[job.order_id]='{"OK":%d}' %counter
                self.job_queue.task_done()
            else:
                logger.info("%d the queue is empty. will sleep 1 minute:%d..." %(id(self.job_queue),self.job_queue.qsize()))
                time.sleep(20)

class LocalFileScanner():
    def __init__(self):
        pass

    def scan(self,relative_folder):
        logger.info(relative_folder)
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

        #TODO how to handle exception? cache single step? or let all break ?
        counter = 0
        for f in filenames:
            iid = cmsService.create_img(self.compose_image(relative_folder,f,aid))
            cmsService.add_order_img(iid,orderid)

            #zoom
            relative_folder_file = relative_folder + '/' + f
            large_relative = self.imageProcessor.thumbnail(relative_folder_file)
            medium_relative = self.imageProcessor.medium(relative_folder_file)
            thumb_relative = self.imageProcessor.large(relative_folder_file)

            img_store = config.img_store
            if img_store == 'oss':
                # upload_file_to_oss(raw_relative_dir+"/"+imgname,(local_tmp_path_pattern%(raw_full_store_dir,imgname)))
                upload_file_to_oss('img'+large_relative,config.img_save_path+large_relative)
                upload_file_to_oss('img'+medium_relative,config.img_save_path+medium_relative)
                upload_file_to_oss('img'+thumb_relative,config.img_save_path+thumb_relative)

            counter += 1

        logger.info('------------------------------done for(%s,%d:%d)---------------------------'%(relative_folder,len(filenames),counter))
        return counter


    def compose_image(self, relative_path, title,aid):
        image = Image(title=title)

        image.file =  relative_path + '/' + title
        image.aid = aid
        image.itype = Image.IMG_TYPE_USER

        return image


def load_local_folder(aid,relative_folder,orderid):
    recordStore = RecordStore(LocalFileScanner())
    return recordStore.process(aid,relative_folder,orderid)


logger.info("......................Initialized...............................")