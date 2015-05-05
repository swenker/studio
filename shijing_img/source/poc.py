__author__ = 'wenjusun'

from httplib import *
import time

httpcon = HTTPSConnection('motocare-sdc200cn.blurdev.com')

request = httpcon.request("GET",'/motocare-portal/web/application/#/home')

response = httpcon.getresponse()

print response.status,":",response.reason

httpcon.close()

time.sleep(5)

print "completed"

