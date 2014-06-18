__author__ = 'samsung'


import unittest
from log_parser import *

v1=[1,1,1]
v2=[1,1,1]
v1=[0,0,1]
v2=[1,1,0]
v1=[1,2,0]
v2=[0,1]
log_parser = LogParser()
class TestLogParser(unittest.TestCase):

    @unittest.skip("Skipping")
    def test_cal(self):
        #print LogParser().calculate_sim_Euclid(v1,v2)
        print log_parser.calculate_sim_Pearson(v1,v2)

    @unittest.skip("Skipping")
    def check_basics(self):
        words=['Hello','WorlD']
        return [w.lower() for w in words]

    @unittest.skip("Skipping")
    def test_showbasic(self):
        print self.check_basics()

    @unittest.skip("Skipping")
    def test_calculate_all_sim(self):
        logfile=r"D:\log\3m.svc\20140601.12972"
        lp = LogParser()
        umap = lp.collect_dlrecords(logfile)
        lp.calculate_all_sim(umap)

        print "done"

    @unittest.skip("Skipping")
    def test_parse_item(self):
        logfile=""
        #logparser = LogParser().parse(logfile)
        line="2014-06-01 10:31:40 downloadReport 357630053387836 4038b64c t8cdktvble 3.0.0.10 1 4.3 SM-N900S 366 77 1"
        nline=line.strip()
        fields=nline.split()
        uid=fields[5]
        itemid=fields[10]
        mid=fields[11]

        print uid,itemid,mid

    @unittest.skip("Skipping")
    def test_cal_based_map_Euclid(self):
        m1={'77': 1, '68': 1, '43': 1, '49': 1}
        m2={'60': 1, '56': 1, '73': 1, '50': 1}
        print LogParser().calculate_sim_map_Euclid(m1,m2)


    @unittest.skip("Skipping")
    def test_cluster(self):
        log_parser.cluster("cal_result.txt")

    def test_cluster2(self):
        log_parser.cluster2("cal_result.txt")

    @unittest.skip("Skipping")
    def test_call_function(self):
        fname="abc"

        fname()

    def test_tree_display(self):
        root = TreeNode("1",None)
        tree = Tree(root)

        leftn=TreeNode("2",root)
        rightn=TreeNode("3",root)
        rightn2=TreeNode("31",rightn)
        #rightn.add_child(rightn2)

        tree.add(leftn)
        tree.add(rightn)
        tree.add(rightn2)

        tree.display()

def abc():
    print "I am abc"

if __name__== "__main__":
    unittest.main()
