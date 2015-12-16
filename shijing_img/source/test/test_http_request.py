__author__ = 'wenjusun'

from httplib import HTTPConnection
from httplib import HTTPSConnection
import threading
import time
import sys

def download(host,path):

    common_httpreq(HTTPConnection(host),path)


def https_download(host,path):

    common_httpreq(HTTPSConnection(host),path)


def common_httpreq(httpcon,path):

    while True:
        httpcon.connect()

        httpcon.request('HEAD',path)

        resp = httpcon.getresponse()

        if(resp.status != 200):
            print "Failed: %d,%s" % (resp.status,resp.reason)

        time.sleep(10)

        httpcon.close()
        

def get_current_time_inmills():
    return int(round(time.time()*1000))

if __name__ == '__main__':
    #https://accounts.motorola.com.cn/ssoauth/login
    host = 'accounts.motorola.com.cn'
    path = '/ssoauth/login'

    LOOPS=1

    """
    print sys.argv
    if sys.argv:
        if len(sys.argv) == 4:
            host = sys.argv[1]
            path = sys.argv[2]
            LOOPS = int(sys.argv[3])
        else:
            print "Please both input host and path,loops "
            exit(0)
    else:
        print "Please input host and path,loops "
        exit(0)
    """
    print time.ctime()

    start_time_inmills = get_current_time_inmills()

    thread_list=[]
    for i in range(0,LOOPS):
        # t = threading.Thread(target=download,args=(host,path,i))
        t = threading.Thread(target=https_download,args=(host,path,i))
        thread_list.append(t)

    for t in thread_list:
        t.start()
        pass

    for t in thread_list:
        t.join()
        pass

    print time.ctime()
    print "total cost:%d seconds" % (get_current_time_inmills()-start_time_inmills)
