__author__ = 'samsung'

print "I am importee"

a="body"

print a
def init():
    global a
    a ="arm"

print a

_hide=None
class Config():
    def __init__(self,vv):
        self.v=vv


config = Config("newv")
def init2():
    pass


