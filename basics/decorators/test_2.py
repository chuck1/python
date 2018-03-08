#!/usr/bin/env python3

class Base(object):

    def __init__(self, f):
        print('__init__',(f,))

    def __call__(*args):
        print('__call__',args)


class Foo(object):
   
    @Base
    def func(self, a):
        print("Foo.func")

print('before creating object')

f=Foo()

print('before falling func')

f.func(1)


