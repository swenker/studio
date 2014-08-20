__author__ = 'sunwj'

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def say(self):
        print "I am Person:%s" % self.name


class Police(object, Person):
    def __init__(self,name,age):
        #super(self,name,age)
        Person.__init__(self,name,age)
        self.job="Police"

    def say(self):
        super(Police,self).say()
        print "I am %s:%s" % (self.job,self.name)


def test_heirichy():
    man = Person("John",30)
    man.say()

    police = Police("Mkie",32)
    police.say()

class TestClassMethod():

    @classmethod
    def foo(cls):
        print "Class method"
        #foo=classmethod(foo)

    @staticmethod
    def foo2():
        print "static method"

        #foo2=staticmethod(foo2)

#import decorator


def mydecorator(func):
    print "I am doc."
    return func

@mydecorator
def show_method():
    TestClassMethod.foo()
    TestClassMethod.foo2()

#show_method()

#compare with the above mydecorator
def decorator2(who):
    def prefix(old_func):
        def new_func(target):
            print who,old_func(target)
        return new_func
    return prefix

@decorator2('man')
def sayHelloTo(her):
    print ",hello,"+her

sayHelloTo("bing")

