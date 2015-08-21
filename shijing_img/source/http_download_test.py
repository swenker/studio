__author__ = 'wenjusun'

from httplib import HTTPConnection
import threading
import time
import sys

def download(host,path,n):
    file_name = path.split('/')[-1] +'_' +str(n)

    httpcon = HTTPConnection(host)

    httpcon.connect()

    httpcon.request('GET',path)

    resp = httpcon.getresponse()

    if(resp.status != 200):
        print "Failed: %d,%s" % (resp.status,resp.reason)
    file_size = int(resp.getheader('Content-Length'))
    print file_size

    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    time.sleep(1)
    local_file = open(file_name,'wb')

    file_size_dl = 0
    buffer_size=8192

    i=0
    while True:
        buffer = resp.read(buffer_size)
        if not buffer:
            break

        i+=1
        if i%10 ==0:
            time.sleep(1)

        local_file.write(buffer)
        file_size_dl +=len(buffer)
        status = r"T-%d %10d  [%3.2f%%]" % (n,file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    httpcon.close()
    local_file.close()

def get_current_time_inmills():
    return int(round(time.time()*1000))

if __name__ == '__main__':

    #host = 'ota-wat-s-mmi.chinacloudapp.cn'
    host = 'stm-d-mmi.chinacloudapp.cn'
    #path='/test.txt'
    path = '/apache-jetty-7.6.1.blur.tar.gz'
    #path = '/jetty-distribution-7.6.16.v20140903.tar.gz'

    LOOPS=20

    print sys.argv
    if sys.argv:
        if len(sys.argv) == 4:
            host = sys.argv[1]
            path = sys.argv[2]
            LOOPS = sys.argv[3]
        else:
            print "Please both input host and path,loops "
            exit(0)
    else:
        print "Please input host and path,loops "
        exit(0)

    print time.ctime()

    start_time_inmills = get_current_time_inmills()

    thread_list=[]
    for i in range(0,LOOPS):
        t = threading.Thread(target=download,args=(host,path,i))
        thread_list.append(t)

    for t in thread_list:
        t.start()
        pass

    for t in thread_list:
        t.join()
        pass

    print time.ctime()
    print "total cost:%d seconds" % (get_current_time_inmills()-start_time_inmills)
