__author__ = 'wenjusun'

import sys
import httplib

#url_pattern = 'http://dspipeline.appspot.com/guide/passport?serialnumber=%s&since=%d'
host = "dspipeline.appspot.com"
url_pattern = "/guide/passport?serialnumber=%s&since=%d"

class GetCheckinData():
    def __init__(self):
        self.httpconn = httplib.HTTPConnection("dspipeline.appspot.com")

    def download(self,sn):

        self.httpconn.connect()
        url = url_pattern %(sn,0)
        self.httpconn.request("GET",url)
        resp = self.httpconn.getresponse()

        if resp.status == 200:
            data = resp.read()
            print data
        elif resp.status == 302:

            newLocation = resp.getheader('Location')

            resp.close()
            self.httpconn.close()

            newconn = httplib.HTTPSConnection('accounts.google.com')
            newconn.connect()
            newconn.request('GET','/ServiceLogin?service=ah&amp;passive=true&amp;continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttp%3A%2F%2Fdspipeline.appspot.com%2Fguide%2Fpassport%253Fserialnumber%253DZX1G722SVM%2526since%253D0&amp;ltmpl=gm&amp;shdf=Ch8LEgZhaG5hbWUaE0xvdHVzIERhdGEgUGlwZWxpbmUMEgJhaCIUb26gW8697YZqLAIgv-XeroOIq0coATIUwkNS3ZuckPqLLAvvbRLyici_Zho')

            newresp = newconn.getresponse()

            print newresp.status,newresp.reason,newresp.read()

            newresp.close()
            newconn.close()

        else:
            print "ERROR:%d,%s,%s" %(resp.status,resp.reason,resp.read())


if __name__ == "__main__":
    sn = ''
    if len(sys.argv) >1 :
        sn = sys.argv[1]

        gcd = GetCheckinData()
        gcd.download(sn)

    else:
        print "Please given sn."





