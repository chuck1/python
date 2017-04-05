#!/usr/bin/env python

class Base(object):

    def __init__(self):
        self.registry = list()

    def register(self, name):
        self.registry.append(name)

    @classmethod
    def wrapper(cls, func):
        print "wrapper"

        def wrapped(self):
            print "wrapped"

            self.register(func.__name__)

            return func(self)

        return wrapped

class Foo0(Base):
   
    @Base.wrapper
    def fun(self):
        print "fun0"

class Foo1(Foo0):

    @Base.wrapper
    def fun(self):
        print "fun1"

f0=Foo1()
f1=Foo1()

f0.fun()

print f0.registry
print f1.registry

