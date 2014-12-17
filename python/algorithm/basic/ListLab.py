__author__ = 'sunwj'


def comp(n,m):
    pnm=1
    for i in range(n-m+1,n+1):
        # print i,

        pnm*=i

    # print pnm
    pm = 1
    print
    for i in range(1,m+1):
        # print i,
        pm *= i

    # print pm
    return pnm/pm


def test_comp():
    print comp(4,3)
    print comp(4,2)
    print comp(3,1)
    print comp(3,2)


def select_tuple(a,m):
    "select tuple with width m from a"


if __name__=='__main__':
    test_comp()