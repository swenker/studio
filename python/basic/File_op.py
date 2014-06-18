
"File operation exercise"
filename="D:\work\python\lab.py"
def read_display1():    
    myfile=open(filename)
    try:
        for line in myfile:
            print line,
    except:        
        myfile.close()
    
def read_display2( ):
    with  open(filename) as myfile:
        for line in myfile:
            print line,
            
def read_display3( ):
    for line in open(filename):
        print line,
            
#read_display1()        

#read_display2()        

read_display3()        

        
