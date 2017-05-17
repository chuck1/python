#!/usr/bin/env python

def wrapper(func):
    print "wrapper"
    print "func =", repr(func)

    def wrapped(self):
            print "wrapped"
            print "func =", repr(func)
            #print "self =", repr(self)
            #print "self.__class__         =", repr(self.__class__)
            name = func.__name__
            mro = self.__class__.__mro__
    
            print "self.__class__.__mro__"
            for cls in mro:
                print "  cls  =", repr(cls)
                if cls == self.__class__: continue
    
                try:
                    f = getattr(cls, name)
                except:
                    pass
                else:
                    f1 = cls.__dict__.get(name)
    
                    print "    func =", repr(f)
                    print "    f1   =", repr(f1)
    
                    print (f is func)
                    print (f1 is func)
    
                    #f1(self)
    
                    #f(self)
    
                    if cls == self.__class__:
                        pass
                    else:
                        print "   ", repr(cls), "is not self.__class__"
    
                        print "    calling"
    
                        #f(self)
        
                    supermeth = getattr(super(cls, self), name, None) 
    
                    print "    supermeth =", repr(supermeth)
            
            s = super(self.__class__, self)
            #print "super =", repr(s)
            #print "super.__class__ =", repr(s.__class__)
            #s = super(
            
            #s_f = s.__getattribute__(func.__name__)
            #s_f = s.fun
    
            #print "func.__name__ =", repr(name)
            #print "super func    =", repr(s_f)
    
            #s_f()
    
            func(self)

    return wrapped

class Foo0(object):

    @wrapper
    def fun(self):
        print "fun0"

class Foo1(Foo0):

    @wrapper
    def fun(self):
        print "fun1"

print "call fun"
f=Foo1()


print f.fun
f.fun()


