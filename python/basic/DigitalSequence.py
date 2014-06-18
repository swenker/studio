
"""
get the index left to which the sum is equal to the right part.
"""
 
def getIndex(a):
    if (len(a)<2):
        return -1
    
    if len(a)==3:
        if a[0]==a[2]:
            return 1
        else:
            return -1
    
    
    total=0
    
    for i in a:
        total +=i
    
    #print total
    
    leftSum=0
    rightSum=total-a[0]  
     
    for i in range(1,len(a)-2):
        leftSum+=a[i-1]
        rightSum-=a[i]
        
        if leftSum==rightSum:
            return i
        
        
    return -1

alist=[-1, 7, 3, 2, 4]    
print getIndex(alist)

alist=[-1, 7, 3, 2, 4,5]    
print getIndex(alist)

alist=[3, 7, 3]    
print getIndex(alist)
