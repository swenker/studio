__author__ = 'wenjusun'

from httplib import *
import time
import json

import threading

def test_http():
    httpcon = HTTPSConnection('motocare-sdc200cn.blurdev.com')

    request = httpcon.request("GET",'/motocare-portal/web/application/#/home')

    response = httpcon.getresponse()

    print response.status,":",response.reason

    httpcon.close()

    time.sleep(5)

    print "completed"


def test_python():
    #import sys
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    kv_file='/home/wenjusun/Localizer_zh_CN_20150618.js'
    jsonfile='/home/wenjusun/resources-locale_default.js'

    kv_map = {}
    with open(kv_file,'r') as f:
        lines = f.readlines()

        for line in lines:
            sl=line.strip().split(" = ")

            skey = sl[0][3:].strip()
            svalue = sl[1].strip(';').strip()

            # if sl[0].count('activation_date_label')>0:
            #     print sl[0][3:].strip()
            #     print skey,svalue.strip('"')

            kv_map[skey]=svalue.strip('"')


    with open(jsonfile,'r') as f:
        poj = json.load(f)

        for item in poj:
            # print type(item)
            # print item['key'] ,item['value']
            skey = item['key']
            # item['value'] = kv_map[skey].decode("UTF-8")
            item['value'] = kv_map[skey]
            #break

        with open('/home/wenjusun/new_resources-locale_default.js','w') as jsonout:

            json.dump(poj,jsonout,ensure_ascii=False,indent=4)
            # js = json.dumps(poj,ensure_ascii=False,indent=4)


    print "Done"


def list_arguments(*params):
    print params

def dict_arguments(**params):
    # print alist
    print params

def test_config_parser():
    from ConfigParser import ConfigParser
    configParser = ConfigParser()
    configParser.read('pwd.cfg')
    # print configParser.get('deployer','azureuser')


class MyBatchHandler(threading.Thread):
    def run(self):
        print "--------------"




if __name__ =='__main__':
    # test_python()
    # list_arguments(1,2,3) #workable

    dict_arguments(**{'a':1,'b':2})

    mythread = MyBatchHandler()
    mythread.start()


