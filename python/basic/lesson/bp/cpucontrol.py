__author__ = 'samsung'

import time



def test():
    i=0
    while(True):

       if(i %2==0):
           i+=1
           print i
       else:
           time.sleep(1)

def test2():
    i=2
    while(True):
        i*=i
        time.sleep(1)
        #print i

def test3():
    while(True):
        i=2
        starttime=int(round(time.time() * 1000))
        ctime=starttime
        while( ctime<(starttime+5)):
            i+=1
            ctime=int(round(time.time() * 1000))

        print i
        time.sleep(0.01)
        print i

test3()