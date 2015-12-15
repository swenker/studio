__author__ = 'wenjusun'


import web
import sys

db = web.database(dbn='mysql',db='cas_statistics',host='localhost',user='motodbu',passwd='idm1512d')
EVENT_TYPES={'0':'login','1':'signup','2':'verify_email'}
class DataProcessor():
    def __init__(self,dtstr):
        self.dtstr = dtstr

    "1159,159,19"
    def parse(self,result):
        items=[]

        event_type_index=0
        for event_count in result.split(','):
            items.append((self.dtstr, event_count, event_type_index))
            event_type_index += 1

        return items

    "2015-09-01,1159,159,19"
    def parse_everyday(self,result):
        items=[]

        event_type_index=0
        elements = result.split(',')
        daystr = elements[0]
        for i in range(1,len(elements)):
            items.append((daystr, elements[i], event_type_index))
            event_type_index += 1

        return items

    def save_to_db(self,items):

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

    def bactch_to_db(self,*data_files):
        t = db.transaction()
        sqls = "INSERT INTO cas_user_counter_daily_test(event_date,count,event_type)values($event_date,$count,$event_type)"

        try:

            for file in data_files:
                with open(file,'r') as f:
                    for each_line in f:
                        # print each_line.strip()
                        items = self.parse_everyday(each_line.strip())
                        # print items
                        for item in items:
                            db.query(sqls,vars={'event_date':item[0],'count':item[1],'event_type':item[2]})


            t.commit()
        except BaseException,e:
            t.rollback()


"Not finished yet."
class DataAnalysis():
    def query(self,start_date,end_date):
        result = db.query('SELECT event_date,count,event_type FROM cas_user_counter_daily')
        records_map={}
        if result:
            for r in result:
                event_date = r[0]
                event_count = r[1]
                event_type = r[2]

                if records_map.has_key(event_date):
                    one_day_events = records_map.get(event_date)
                    records_map[event_date] = one_day_events.apend(event_count)

                else:
                    records_map[event_date]=[event_count]


    def to_csv(self,records, csv_filepath,):
        with open(csv_filepath,'w') as csv_file:
            csv_file.write(records)

        print "Done."

if __name__=='__main__':

    dp = DataProcessor(sys.argv[1])
    # dp.bactch_to_db('cas_2015-09.txt','cas_2015-10.txt')
    dp.handle_statistics(sys.argv[2])


