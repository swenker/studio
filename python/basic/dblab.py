#! /usr/bin/env python
#coding=utf-8
import MySQLdb
connection=MySQLdb.connect(user='root',db='test')


def create_table():
    mycur=connection.cursor()
    mycur.execute("create table ptest(tname varchar(20))")
    mycur.close()

def insert_data():
    mycur=connection.cursor()
    mycur.execute("insert into ptest(tname)values('tn01')")
    mycur.execute("insert into ptest(tname)values('tn02')")
    mycur.close()
    
    print "data inserted.."
        

def list_data():
    mycur=connection.cursor()
    mycur.execute("select * from ptest")
    
    name_to_index = dict((d[0], i) for i, d in enumerate(mycur.description)) 
    print name_to_index
    for data in mycur.fetchall():
        print data[name_to_index['tname']],
        #for dcol in data:
            #print dcol,
        #print "\n"
        
    print "data listed..."
    
#insert_data()
list_data()


try:
    connection.commit()
except:
    connection.rollback()
finally:
    connection.close()

