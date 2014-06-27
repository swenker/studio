# _*_ coding: UTF-8 _*_
__author__ = 'samsung'

nums=raw_input("five dig:")

print nums

promptstring="Please input your choice:\n" \
             "1.add\n" \
             "2.average\n" \
             "0.exit\n"
print promptstring

opt=raw_input()
while(opt and opt!="0"):
    sum=0
    if opt=="1":
        for i in nums.split(","):
            sum+=int(i)

        print sum

    elif opt=="2":
        for i in nums.split(","):
            sum+=int(i)
        avg=sum/5.0
        print avg

    opt=raw_input()



