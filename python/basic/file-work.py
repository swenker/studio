#! /usr/bin/env python
#coding=utf-8

def display_file(fname,nline):
    i=0
    f = open(fname,'r')
    try:
        
        for line in f:
            if not line.startswith('#'):
                print line,
                i+=1
            
            if i==nline:
                break
        
    except IOError,ioe:
        print ioe,
        
    finally:                
        f.close()    

fname = str(raw_input("please input file:\n"))

print fname

nline = int(raw_input("please input n:\n"))

print nline
               
display_file(fname,nline)

print "%s\n" % "ended."        
        