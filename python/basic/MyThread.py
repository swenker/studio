#! /usr/bin/env python
#coding=utf-8

import threading
import datetime
import time
import Queue
import urllib2

class MyThread(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s say Hello at time:%s"   %(self.getName(),now)
        
def play():
    for i in range(2):
        t =   MyThread()
        t.start()        


hosts=('http://www.samsung.com','http://www.samsung.net','http://www.bing.com')
class HtmlCrawler(threading.Thread):
    
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
   
    def run(self):
        while True:
            host = self.queue.get()
            website=urllib2.urlopen(host)
            print website.read(1024)
            #TODO close the url?
            
            self.queue.task_done()

starttime=time.time()

def engine():
    
    websiteQueue=Queue.Queue()
    for i in range(2):
        htmlCrawler = HtmlCrawler(websiteQueue)
        htmlCrawler.setDaemon(True)
        htmlCrawler.start()
    
    for h in hosts:
        websiteQueue.put(h)

    websiteQueue.join()
    
engine()

print "%d time elapsed" %(time.time()-starttime)
             
