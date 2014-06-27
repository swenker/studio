__author__ = 'samsung'
#!/bin/env python
#coding=utf-8
"Get local Configruation info and report it to remote admin server."

import socket
import os
import subprocess
import httplib
import urllib


class NetworkInfo:

    def __init__(self):
        self.hostname=socket.gethostname()
        self.wip=None
        self.lip=None

        network_scripts0='/etc/sysconfig/network-scripts/ifcfg-eth0'
        network_scripts1='/etc/sysconfig/network-scripts/ifcfg-eth1'

        if(os.path.isfile(network_scripts0)):
            self.lip = self.get_ipaddr(network_scripts0)

        if(os.path.isfile(network_scripts1)):
            self.wip = self.get_ipaddr(network_scripts1)


    def get_ipaddr(self,fp):
        "IPADDR=121.197.3.120"
        ip=None
        try:
            with open(fp,"r") as nif:
                for line in nif:
                    if (line.startswith("IPADDR=")):
                       ip=line[7:]
                       break;
        except IOError:
            print IOError.message

        return ip


    def get_hostname(self):
        return self.hostname

    def get_lip(self):
        return self.lip

    def get_wip(self):
        return self.wip


class HardwareInfo:
    def __init__(self):
        self.diskinfo={}
        self.cpuinfo={}
        self.meminfo={}

        part1="/dev/xvda1"
        part2="/dev/xvdb1"

        self.diskinfo[part1]=self.get_diskinfo(part1)

        if(os.path.exists(part2)):
            self.diskinfo[part2]=self.get_diskinfo(part2)

        self.cpuinfo["cores"] = self.get_cpucores()
        self.meminfo['total']= self.get_totalmem()

    #dodo data structure
    def get_diskinfo(self,part):
        result=subprocess.Popen(["df","-ah",part],stdout=subprocess.PIPE)
        output,err=result.communicate()
        return output

    def get_cpucores(self):
        """  $ cat /proc/cpuinfo """
        cores={}
        with open('/proc/cpuinfo') as f:
            for line in f:
                if (line.startswith("cpu cores")):
                    cores= line.split(":")[1].strip()
                    break
        return cores

    def get_totalmem(self):
        totalMem=0
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    tmp=line[9:].strip()
                    totalMem=tmp[:-3]
                    break
        return totalMem

class Agent():
    def report(self):
        ni = NetworkInfo()
        hd = HardwareInfo()
        httpcon=httplib.HTTPConnection("lab01.qasvc.mscc.cn",8080)
        try:
            params = urllib.urlencode({'lip': ni.lip, 'wip': ni.wip, 'totalmem': hd.get_totalmem(),'cpu':hd.get_cpucores()})
            headers = {"Content-type": "application/x-www-form-urlencoded",    "Accept": "text/plain"}

            httpcon.request("POST","/c/report",params,headers)
            response=httpcon.getresponse()

            print response.status,response.reason
        except httplib.HTTPException ,e:
            print e.message
        finally:
            httpcon.close()


def testNetworkModule():
    ni = NetworkInfo()
    print ni.get_hostname(),ni.get_lip(),ni.get_wip()

    hd = HardwareInfo()
    #print hd.cpuinfo,hd.diskinfo
    print hd.meminfo

if __name__ =='__main__':
    agent=Agent()
    agent.report()




