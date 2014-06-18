"""
Implementation of some algorithm for string operation
"""

print __doc__    

def checkDup(myStr):    
    #empty list
    ha=[x/x*(-1) for x in range(1,256) ]
    for c in myStr:
        ci=ord(c)
        if ha[ci]!='-1' : 
            print c    
            return True
        
        ha[ci]=c

    return False
 
def checkUnique(myStr):
    flag=0
    for c in myStr:
        ci=ord(c)-ord('a')
        if( flag&1<<ci>0):
            return False
        flag|=1<<ci
    
        
    return True
    
#print "here:%s " % checkUnique('abcdea')


def reverseStr(myStr):
    slen=len(myStr)
    front=0
    rear=slen-1
    
    newStr=['']*slen
    
    while front<rear:
        newStr[front]=myStr[rear]
        newStr[rear]=myStr[front]        
        front+=1
        rear-=1
    newStr[front]=myStr[rear] 
    return ''.join(newStr)

myStr="abcde"
print "The original:%s,reversed:%s" % (myStr,reverseStr(myStr))

myStr="abcd"
print "The original:%s,reversed:%s" % (myStr,reverseStr(myStr))

myStr="ab"
print "The original:%s,reversed:%s" % (myStr,reverseStr(myStr))

myStr="a"
print "The original:%s,reversed:%s" % (myStr,reverseStr(myStr))
