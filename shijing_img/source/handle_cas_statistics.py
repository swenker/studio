__author__ = 'wenjusun'


import web
import sys

class DataProcessor():
    def __init__(self,dtstr):
        self.dtstr = dtstr

    def parse(self,result):
        items=[]

        event_type_index=0
        for event_count in result.split(','):
            items.append((self.dtstr, event_count, event_type_index))
            event_type_index += 1

        return items

    def save_to_db(self,items):
        db = web.database(dbn='mysql',db='cas_statistics',host='localhost',user='motodbu',passwd='idm1512d')

        t = db.transaction()
        try:
            sqls = "INSERT INTO cas_user_counter_daily(event_date,count,event_type)values($event_date,$count,$event_type)"
            for item in items:
                db.query(sqls,vars={'event_date':item[0],'count':item[1],'event_type':item[2]})
            t.commit()
        except BaseException,e:
            t.rollback()

    def handle_statistics(self,log_result):
        parse_result = self.parse(log_result)
        # print parse_result
        self.save_to_db(parse_result)


if __name__=='__main__':

    dp = DataProcessor(sys.argv[1])
    dp.handle_statistics(sys.argv[2])

