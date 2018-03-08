import inspect

def mems(o):
    print o
    for d in dir(o):
        print "  {:32}{:32}".format(str(d),str(getattr(o,d)))

class Base(object):

    @classmethod
    def wrap(cls, func):

        print repr(cls), repr(func)

        for d in dir(func):
            print "  {:32}{:32}".format(str(d),str(getattr(func,d)))

        print inspect.getouterframes(inspect.currentframe())
        print inspect.getouterframes(inspect.currentframe())[1]
        print inspect.getouterframes(inspect.currentframe())[1][0]
        mems(inspect.getouterframes(inspect.currentframe())[1][0])
        mems(inspect.getouterframes(inspect.currentframe())[1][0].f_code)

        #print "func.func_code"
        #for d in dir(func.func_code):
        #    print "  {:32}{:32}".format(str(d),str(getattr(func.func_code,d)))

        def dec(func):
            def wrapped(self):
                return func(self)
            return wrapped
        return dec

class Foo(Base):

    @Base.wrap
    def x(self):
        return 0

class Bar(Foo):

        
    def x(self):
        return 1

#f0 = Foo.x
#f1 = Bar.x

#print f0
#print f0.im_class
#print f1
#print f1.im_class

#f = Foo()

#for d in dir(f):
#    print "{:32}{:32}".format(str(d), str(getattr(f,d)))

