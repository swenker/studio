__author__ = 'sunwj'


import httplib
import urllib
import hashlib

qasvc_url=''
# qasvc_host='push.qasvc.mscc.cn'
qasvc_host='push.qasvc.mcitech.cn'
HTTP_METHOD="POST"


key="22fe3263315576157435d396c913871"
appId="mci-multimediamagazine"

rawParams={"appId":appId,
           "pushType":"2",
           "criteria":"queryType:pushByQuery;pressId:1;magazineId:2;modelType:3;modelName:4;channelId:5;idleDays=1",
           "msgType":"1",
           "msgTitle":"test",
           "msgDesc":"test",
           "msgContent":'{"Id":0,"RefId":33,"URL":"http://www.baidu.com","Message":"test","State":1,"Type":2,"CreateDate":"2014-10-22T16:44:44.8504+08:00","ModifyDate":"2014-10-22T16:44:44.8504+08:00","MagazineId":null,"Title":null}',
           # "msgContent":'',
           "targetId":"2"}

#msgContent=test&msgDesc=test&msgTitle=test&msgType=2&pushType=2&targetId=2&key=22fe3263315576157435d396c913871

rawParams={"appId":appId,
           "pushType":"2",
           "criteria":"test",
           "msgType":"2",
           "msgTitle":"test",
           "msgDesc":"test",
           "msgContent":'test',
           # "msgContent":'',
           "targetId":"2"}

#{"Id":0,"RefId":33,"URL":"http://www.baidu.com","Message":"test","State":1,"Type":2,"CreateDate":"2014-10-22T16:44:44.8504+08:00","ModifyDate":"2014-10-22T16:44:44.8504+08:00","MagazineId":null,"Title":null}

def pushBySubscription():
    httpcon=httplib.HTTPConnection(qasvc_host,8080)

    mysign = gen_sign(rawParams)
    print mysign
    rawParams['sign']= mysign
    params=urllib.urlencode(rawParams)

    headers={"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
    httpcon.request(HTTP_METHOD,'/cpp-push/baidu/push',params,headers)
    response = httpcon.getresponse()
    print response.status,response.reason

    httpcon.close()





def gen_sign(params):
    pkeys=params.keys()
    pkeys.sort()

    print pkeys

    tmps=''
    for k in pkeys:
        tmps+= k+"="+str(params[k])+"&"

    tmps += "key="+key

    print tmps
    #return hashlib.md5(urllib.quote_plus(tmps)).hexdigest()
    return hashlib.md5(tmps).hexdigest()
    # return hashlib.md5("appId=mci-multimediamagazine&bdChannel=4406071778305562052&bdUser=595637424929694025&imei=355848060487165&serialNo=0162c498&key=22fe3263315576157435d396c913871").hexdigest()

#print gen_sign(rawParams)
pushBySubscription()