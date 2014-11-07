__author__ = 'sunwj'

"Get the different ones from two list"

def gen_diff(type,seta,setb):

    setab = seta - setb
    tmps = ''

    for s in setab:
        tmps+=s
        #tmps+="\n"

    #print "a-b"+tmps

    fab = open('/home/sunwj/'+type+'-fab.txt','w')

    fab.writelines(tmps)

    fab.close()

    setba = setb - seta

    tmps = ''

    for s in setba:
        tmps +=s

    #print "b-a"+tmps
    fba = open('/home/sunwj/'+type+'-fba.txt','w')

    fba.writelines(tmps)

    fba.close()

    print "completed\n"


def get_set(filepath):
    rawlist=[]
    with open(filepath) as f:
        for line in f:
            rawlist.append(line)

    #print len(rawlist)
    return set(rawlist)

def generate_diff():
    nd_stsvc="/home/sunwj/nd_stsvc.txt"
    nd_svc="/home/sunwj/nd_svc.txt"

    nd_seta=get_set(nd_stsvc)
    nd_setb=get_set(nd_svc)

    gen_diff('nd',nd_seta,nd_setb)


    da_stsvc="/home/sunwj/da_stsvc.txt"
    da_svc="/home/sunwj/da_svc.txt"

    da_seta=get_set(da_stsvc)
    da_setb=get_set(da_svc)

    gen_diff('da',da_seta,da_setb)


generate_diff()





