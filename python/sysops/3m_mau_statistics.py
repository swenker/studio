__author__ = 'sunwj'

import MySQLdb as mdb
import datetime

dbuser='mscc_reader'
dbpasswd='R1e2a3d4er!'

dbname='sunwj_test'
dbhost='db.qasvc.mscc.cn'

dbcon = None

print datetime.datetime.now()
try:
    dbcon=mdb.connect(dbhost,dbuser,dbpasswd,dbname)

    dbcur=dbcon.cursor()

    #dbcur.execute("SELECT VERSION()");


    query_total_daily = "select count(distinct serial_no) from server_log_201410 where log_date='2014-10-%s' "
    query_normal_daily = "select count(distinct serial_no) from server_log_201410 where log_date='2014-10-%s' and api_name !='dynamicConfig' and api_name !='getMessage' "

    monthv=['']*31

    daily_total=[]
    daily_normal=[]

    for i in range(0,31):
        if(i<9):
            monthv[i] = '0'+str((i+1))
        else:
            monthv[i] = str(i+1)

    for d in monthv:
        sql_total = query_total_daily %d
        sql_normal = query_normal_daily %d

        #print sql_total
        #print sql_normal

        dbcur.execute(sql_total)
        data = dbcur.fetchone()
        #the result is a tuple
        daily_total.append(data[0])
        #print daily_total

        dbcur.execute(sql_normal)
        data = dbcur.fetchone()
        daily_normal.append(data[0])
        #print daily_normal
    print

    for i in range(0,31):
        print "%d:%d,%d,%d" %(i+1,daily_total[i],daily_normal[i],daily_total[i]-daily_normal[i])



except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])

finally:
    if dbcon:
        dbcon.close()

print datetime.datetime.now()