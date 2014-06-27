#uthor__ = 'Wenju'

import httplib
import sys
"""
This is used to inspect the content from mci server.such as the counter of given word.
So several headers' default values are hardcoded at the moment,including appkey and DeviceType
"""

MAX_VALUE=10
MIN_VALUE=0
WARN_VALUE=0
CRITICAL_VALUE=0

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

STATUS_TEXT='OK'
STATUS_CODE=STATE_OK

def getRemoteContent(rhost,api):
    #print rurl
    http_conn = httplib.HTTPConnection(rhost)
    try:
        headers={"appkey":"f93f6bed4y21da73cadebe83c623b4s","DeviceType":"1"}
        http_conn.request("GET", api,headers=headers)
        resp = http_conn.getresponse()
        content = resp.read()
        #print content
        http_status = resp.status
        if (http_status != 200):
            STATUS_CODE=STATE_UNKNOWN
            STATUS_TEXT=http_status
    except Exception,e:
        STATUS_CODE=STATE_UNKNOWN
        #STATUS_TEXT=e.args
        raise
    finally:
        http_conn.close()
    return content

if (len(sys.argv) <4):
    print "Not enough parameters(url,keyword)!"

#surl="http://3m.qasvc.mcitech.cn/api/magazine/list/1/10/0"
#surl="http://%s%s" %(sys.argv[1],sys.argv[2])
rhost=sys.argv[1]
rapi=sys.argv[2]
#sword="RecommendId"
sword=sys.argv[3]
scontent = getRemoteContent(rhost,rapi)

wcount=scontent.count(sword)


print "%s,%s-%d|item=%d,%d,%d,%d,%d" %(STATUS_TEXT,sword,wcount,wcount,WARN_VALUE,CRITICAL_VALUE,MIN_VALUE,MAX_VALUE)

sys.exit(STATUS_CODE)
