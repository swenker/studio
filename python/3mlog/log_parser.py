__author__ = 'samsung'

import os
from math import *

class Tree():
    def __init__(self,root,similarity=1):
        self.root=root
        self.similarity=similarity

    def contains(self,node):
        return self.root.has_node(node)

    def add(self,node):
        if node.id == self.root.id:
            return False

        tnode=self.root.has_node(node)
        if not tnode:
            if node.parent.id == self.root.id:
                self.root.add_child(node)
            else:
                pnode = self.root.has_node(node.parent)
                if not pnode:
                    raise BaseException("parent not exist:"+node.parent.id)
                else:
                    pnode.add_child(node)

    def display(self):
        print "\n[",
        self.root.display()
        print "]"

    def get_all_nodes(self):
        nodes=[]
        sublist=[]
        self.__get_sublist(self.root,sublist)
        nodes +=sublist

        return nodes

    def __get_sublist(self,node,sublist):
         sublist.append(node.id)
         if node.children:
             for chd in node.children:
                 self.__get_sublist(chd,sublist)

class TreeNode():
    def __init__(self,nid,parent):
        self.id=nid
        self.children=[]
        self.parent=parent
        self.chdindex=[]

    def get_sublist(self):
        return self.chdindex

    def add_child(self,chd):
        if chd.id in self.chdindex:
            return False

        self.children.append(chd)
        self.chdindex.append(chd.id)
        chd.parent=self

    def has_node(self,chd):
        "return it"
        if chd.id == self.id:
            return self

        if chd.id in self.chdindex:
            for child in self.children:
                if child.id == chd.id:
                    return child
        elif self.children:
            for child in self.children:
                rschd = child.has_node(chd)
                if rschd:
                    return rschd

            return None
        else:
            return None

    def get_node(self):
        return None

    def display(self):
        print "["+self.id+",",
        if(self.children):
            for chd in self.children:
                chd.display()
        print "]",


class LogParser():

    def calculate_sim_Euclid(self,v1,v2):
        "Euclid distance based"
        similarity=0
        sum=0
        for i in range(len(v1)):
            sum+=pow(v1[i]-v2[i],2)
        similarity=1.0/(1+sqrt(sum))

        return similarity

    def get_vector(self,m1,m2):

        v1 = [0 for x in range(84)]
        v2 = [0 for x in range(84)]
        for mid in m1.keys():
            v1[int(mid)-1] = m1[mid]

        for mid in m2.keys():
            v2[int(mid)-1] = m2[mid]

        return v1,v2

    def calculate_sim_map_Euclid(self,m1,m2):
        "Euclid distance based"

        v1,v2 = self.get_vector(m1,m2)

        return self.calculate_sim_Euclid(v1,v2)


    def calculate_sim_Pearson(self,v1,v2):
        """
            lxy/sqrt(lxx*lyy)
            lxx=sum(x**2)-(sum(x))**2/n
            lyy=sum(y**2)-(sum(y))**2/n
            lxy=sum(x*y)-sum(x)*sum(y)/n
        """
        n=len(v1)
        sumx,sumx2=0,0
        sumy,sumy2=0,0
        sumxy =0

        for i in range(n):
            x=v1[i]
            y=v2[i]

            sumx2+=pow(x,2)
            sumx+=x

            sumy2+=pow(y,2)
            sumy+=y

            sumxy +=x*y

        lxx = sumx2-(pow(sumx,2)/n)
        lyy = sumy2-(pow(sumy,2)/n)
        lxy = sumxy-((sumx*sumy)/n)

        similarity=lxy/sqrt((lxx*lyy))
        return similarity

    def calculate_sim_map_Pearson(self,m1,m2):
        v1,v2 = self.get_vector(m1,m2)
        return self.calculate_sim_Pearson(v1,v2)

    def calculate_sim_map(self,m1,m2):
        return self.calculate_sim_map_Euclid(m1,m2)

    def collect_dlrecords(self,log_file_path):
        print "hello"
        outfile=file("dlrecords2.txt","w")

        ummap={}

        with open(log_file_path) as f:
            for line in f:
                if line.count("downloadReport"):
                    #the line still contains line separator?

                    #2014-06-01 10:31:40 downloadReport 357630053387836 4038b64c t8cdktvble 3.0.0.10 1 4.3 SM-N900S 366 77 1
                    nline=line.strip()
                    fields=nline.split()
                    uid=fields[5]
                    if uid=='-':
                        continue

                    itemid=fields[10]
                    mid=fields[11]

                    if ummap.has_key(uid):
                        midmap=ummap[uid]
                        if midmap.has_key(mid):
                            midmap[mid] +=1
                        else:
                            midmap[mid]=1

                        ummap[uid]=midmap

                    else:
                        if mid:
                            ummap[uid]={mid:1}


            for key in ummap.keys():
                tmap=ummap[key]

                oline = "%s,%s \n" %(key,tmap)

                outfile.write(oline)

        outfile.close()
        return ummap

    def calculate_all_sim(self,ummap):
        ukeys=ummap.keys()

        outfile=open("cal_result.txt","w")

        i=-1
        for i in range(0,len(ukeys)):
            #for base_uid in ukeys:
            base_uid=ukeys[i]
            m1=ummap[base_uid]

            for j in range(1+i,len(ukeys)):
                #for target_uid in ukeys:
                target_uid = ukeys[j]
                m2 = ummap[target_uid]

                similarity=self.calculate_sim_map(m1,m2)
                result = "%s,%s,%s\n" %(base_uid,target_uid,similarity)
                outfile.write(result)

        outfile.close()


    def cluster(self,records_file):
        "tspib96xuz,mkcjz4sxmw,0.0978517197297"
        kmap={}
        with open(records_file) as f:
            for line in f:
                fields = line.strip().split(",")
                key = fields[0]+"-"+fields[2]
                pair=fields[1]
                if not fields[2]=="1.0":
                    continue

                if not (kmap.has_key(key)):
                    kmap[key] = []

                kmap[key].append(pair)

        cluster_file=open("cluster.txt","w")
        try:
            for k,v in kmap.items():
                cluster_file.write(("%s,%s\n" %(k,v)))
        except IOError,io:
            print io
        finally:
            cluster_file.close()

        print len(kmap)

    def intree(self,treelist,node):
        for tree in treelist:
            tnode=tree.contains(node)
            if tnode:
                return tree,tnode
        return None,None
    #TODO optimize the logic
    def cluster2(self,records_file):
        "tspib96xuz,mkcjz4sxmw,0.0978517197297"
        treelist=[]
        with open(records_file) as f:
            for line in f:
                fields = line.strip().split(",")
                key = fields[0]
                pair=fields[1]
                if not fields[2]=="1.0":
                    continue

                pnode = TreeNode(key,None)
                subnode=TreeNode(pair,pnode)
                tree,tnode=self.intree(treelist,pnode)
                if not tree:
                    stree,stnode = self.intree(treelist,subnode)
                    if not stree:
                        tree = Tree(pnode)
                        tree.add(subnode)
                        treelist.append(tree)
                    else:
                        pnode=TreeNode(pair,stnode)
                        stree.add(pnode)
                else:
                    if tree.contains(subnode):
                        continue
                    else:
                        tree.add(subnode)


        print len(treelist)
        for t in treelist:
            t.display()
            #print "======",
            #print t.get_all_nodes()

