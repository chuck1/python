#!/usr/bin/env python3

def outer(*args):
    print('outer',args)
    def wrapper(*args1):
        print('wrapper',args1)
        def wrapped(*args2):
            print('wrapped',args2,args1,args)
    
        return wrapped

    return wrapper

class Foo(object):
   
    @outer(2)
    def func(self, a):
        print("Foo.func")

print('before creating object')

f=Foo()

print('before falling func')

f.func(1)


