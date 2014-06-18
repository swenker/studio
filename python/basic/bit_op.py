#! /usr/bin/env python
#coding=utf-8

max = ~0
i,j = 2, 6

n=0
m=0



left = max - ((1 << j) - 1)

#print "left1:",bin((1 << j)-1 )

print "max:%s,left:%s" %(bin(max),bin(left))

right = ((1 << i) - 1)

print "right:",bin(right)
mask = left | right

print "mask:",bin(mask)

result = (n & mask) | (m << i)

print result


