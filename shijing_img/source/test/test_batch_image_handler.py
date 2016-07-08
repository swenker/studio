__author__ = 'wenjusun'

import os,sys
import unittest
import threading
import time
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from cms.batch_image_handler import *



class RequestSenderThread(threading.Thread):


    def __init__(self,order_id,relative_folder,group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(RequestSenderThread, self).__init__(group, target, name, args, kwargs, verbose)


    def run(self):
        i = 0
        while(i<3):
            pj = PhotoJob(int('11'+str(i)),'/2015/'+str(i)+'/20',1)
            submit_job(pj)

            i+=1
            time.sleep(10)



class TestBatchImageHandler(unittest.TestCase):
    def test_send_handle_order_photo(self):
        rst = RequestSenderThread(11,'/2011/12/13')
        rst.start()
        print
        print "sender started."



if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(CmsServiceTestCase)
    suite = unittest.TestSuite()
    tests = ['test_send_handle_order_photo']
    for test in tests:
        suite.addTest(TestBatchImageHandler(test))

    unittest.TextTestRunner(verbosity=2).run(suite)

    time.sleep(30)



