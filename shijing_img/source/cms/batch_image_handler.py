__author__ = 'wenjusun'

import threading
import time
import glob
import os

import web
import cms_utils
import cms_service
from cms_model import *
from aliyun_oss_handler import *
from image_processor import ImageProcessor
from backend_service_helper import *

"""
    to deal with those images batch uploaded?
    the images will be manually uploaded to a folder /raw/.....
"""

cmsService = cms_service.cmsService
logger = config.getlogger('batch_image_handler')

db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=config.passwd, charset="UTF-8")
# db = web.database(dbn=config.dbn, db=config.db, host=config.host, user=config.user, passwd=cms_utils.decrypt(config.passwd,config.passwd_padding))
db.printing=config.web_debug

TABLE_JOB="shijing_jobs"


completed_tasks={}

import Queue
class JobService_deprecated():
    job_queue = Queue.Queue()
    def submit_job(self,job):
        JobService_deprecated.job_queue.put(job)
        print "submit job :",
        print os.getpid()
        # print JobService_deprecated.job_queue

    def handle_jobs(self):
        while True:
            print "thread process id:",
            print os.getpid()
            completed_tasks[11]='123'
            print completed_tasks
            print JobService_deprecated.job_queue
            if not JobService_deprecated.job_queue.empty():
                job = JobService_deprecated.job_queue.get_nowait()
                logger.info("------------got job:%d" %job.order_id)

                counter = 1
                # counter = load_local_folder(job.album_id,job.relative_folder,job.order_id)
                print "=============================================I am a task========================="
                completed_tasks[job.order_id]='{"OK":%d}' %counter
                JobService_deprecated.job_queue.task_done()
                print completed_tasks
            else:

                logger.info("the queue is empty. will sleep 1 minute:%d..." %(JobService_deprecated.job_queue.qsize()))
                time.sleep(20)

    def start_worker_thread(self):
        worker_thread = threading.Thread(target=self.handle_jobs)
        worker_thread.setDaemon(True)
        worker_thread.start()


class JobService():
    def submit_job(self,job):
        sqls = """INSERT INTO %s(job_name,job_data,job_status)VALUES($name, $jobdata, $status)""" %TABLE_JOB
        t = db.transaction()
        job_id = -1
        try:
            db.query(sqls,vars={"name": job.name, "jobdata": job.jobdata, "status": job.status})

            result = db.query("select LAST_INSERT_ID() AS mid ")
            if result:
                job_id = result[0]['mid']

            t.commit()
        except StandardError as error:
            t.rollback()

        logger.info("submitted job:name=%s,jobid=%d" % (job.name,job_id) )
        return job_id

    def handle_jobs(self):
            while True:
                sqls = "SELECT id FROM  %s WHERE job_status=1 ORDER BY id LIMIT 1" % TABLE_JOB
                result = db.query(sqls)
                if result:
                    job_id =result[0]['id']
                    transaction = db.transaction()
                    sqls = "SELECT * FROM %s WHERE id=$job_id FOR UPDATE " %TABLE_JOB
                    try:
                        query_record = db.query(sqls,vars={'job_id':job_id})
                        job_record = query_record[0]
                        photojob =PhotoJob(**json.loads(job_record['job_data']))

                        logger.info("------------got job:%d" %job_id)

                        counter = load_local_folder(photojob.album_id,photojob.relative_folder,photojob.order_id)

                        sqls = "UPDATE %s SET dtcomplete=$dtc, job_status=$status,job_result=$job_result WHERE id=$job_id " %TABLE_JOB
                        job_result = '{"status":9,"reason":"%d processed"}' % counter
                        db.query(sqls,vars={'dtc':get_timenow(),'status':9,'job_id':job_id,'job_result':job_result})

                        logger.info("Job(id=%d) completed: -- counter:%d " %(job_id,counter))

                    finally:
                        sqls = "UPDATE %s SET dtupdate=$dtc WHERE id=$job_id " %TABLE_JOB
                        db.query(sqls,vars={'dtc': get_timenow(),'job_id':job_id})
                        transaction.commit()

                        time.sleep(1*60)

                else:
                    # logger.info("no tasks to be processed this loop")
                    time.sleep(1*60)

    #TODO query by order id? or there should be an extra table from order side to store the relation
    def get_job_status(self,job_id):
        sqls = "SELECT job_result FROM %s WHERE id=$job_id " %TABLE_JOB
        result = db.query(sqls,vars={'job_id':job_id})

        if result:
            job_result = result[0]['job_result']
            if job_result:
                return job_result

        return ''


    def start_worker_thread(self):
        worker_thread = threading.Thread(target=self.handle_jobs)
        worker_thread.setDaemon(True)
        worker_thread.start()


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
        cmsService.update_order_img_counter(orderid,counter)

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