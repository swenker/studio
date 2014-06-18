
#coding=UTF-8
import sys

"""
1 请将a字符串的数字取出，并输出成一个新的字符串。
2 请统计a字符串出现的每个字母的出现次数（忽略大小写，a与A是同一个字母），并输出成一个字典。 例 {'a':3,'b':1}
3 请去除a字符串多次出现的字母，仅留最先出现的一个,大小写不敏感。例 'aAsmr3idd4bgs7Dlsf9eAF'，经过去除后，输出 'asmr3id4bg7lf9e'
"""

a = "aAsmr3idd4bgs7Dlsf9eAF"
print a


def print_unique():
    a_dict={}
    for c in a:
        ci=ord(str(c).lower())
        #print a_dict.get(ci)
#        print '%s:%d' %(c,ci)
            
        if(97<=ci<=122): #a-z A-Z
            if(a_dict.get(ci)):
                #print ",%s" %(a_dict[ci]),
                pass
            else:
                sys.stdout.write(c)
                a_dict[ci]=c
        else:
            sys.stdout.write(c)
                        
print_unique()
   
def print_digital():
    
    a_digital=''
    for i in a:
        if(47<ord(i)<58):
            print i
            a_digital+=str(i)
            
    print a_digital
    
#print_digital()

def print_occurency():
    a_c={}
    for c in a:
        tc=str(c).lower()
        if(97<ord(c)<122):
            cv=a_c.get(tc)
            if( cv>0 ):            
                a_c[tc]+=1
            else:
                a_c[tc]=1
            
    print a_c
            
#print_occurency()            


            
    
