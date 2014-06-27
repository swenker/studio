__author__ = 'samsung'

import web
import datetime

db = web.database(dbn="mysql",db="server_config",host="demodb01.qasvc.mscc.cn",user="sconf",passwd="host321",charset='utf8')
TABLE_CONFIG="sc_config"
COLUMN_LIP="lip"
COLUMN_WIP="wip"
COLUMN_TOTALMEM="totalmem"
COLUMN_CPU="cpu"

class Config():
    def __init__(self,lip,totalmem,cpu,wip):
        self.lip=lip
        self.totalmem =totalmem
        self.cpu=cpu
        self.wip=wip

    def __str__(self):
        return "Config[lip:%s;wip:%s;totalmem:%d;cpu:%d]" %(self.lip,self.wip,self.totalmem,self.cpu)


def saveconfig(config):
    #get lip and check if it exist
    lip=config.lip
    result=db.query(db.select(TABLE_CONFIG,where='lip=$lip',vars=locals()))
    if(result or len(result)>0):
        updateconfig(lip,config)
    else:
        insertconfig(lip,config)

def insertconfig(lip,config):
    db.insert(TABLE_CONFIG,lip=lip,wip=config.wip,totalmem=config.totalmem,cpu=config.cpu,dt_update=datetime.datetime.now())

def updateconfig(lip,config):
    db.update(TABLE_CONFIG,where='lip=$lip',vars=locals(),wip=config.wip,totalmem=config.totalmem,cpu=config.cpu,dt_update=datetime.datetime.now())


def getconfigbylip(lip):
    result=db.select(TABLE_CONFIG, where='lip=$lip', vars=locals())
    if(result):
        return  Config(lip,result[COLUMN_TOTALMEM],result[COLUMN_CPU],result[COLUMN_WIP])

    return None

def getconfiglist():
    result=db.select(TABLE_CONFIG, order=COLUMN_LIP)
    items=[]
    if(result):
        for item in result:
           conf=Config(item[COLUMN_LIP],item[COLUMN_TOTALMEM],item[COLUMN_CPU],item[COLUMN_WIP])
           items.append(conf)

    return  items

def test():
    testconf=Config("10.200.115.123",'8012',2,"121.197.2.169")
    saveconfig(testconf)
    print getconfiglist()


if __name__=="__main__":
    test()