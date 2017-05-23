

class Foo(object):
    def __init__(self):
        pass

    a = 1
    b = 2

    def __getattribute__(self, name):
        if name == 'a':
            return object.__getattribute__(self, name)
        else:
            print("not allowed {}".format(name))

    def __setattr__(self, name, v):
        print('setattr ' + name)
        object.__setattr__(self, name, v)


foo = Foo()

foo.a
foo.b

class Bar(Foo):
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

bar = Bar()

print(bar.a)
print(bar.b)

def ga(o, name):
    print('ga')
    
def sa(o, name, v):
    print('sa')

foo.__getattribute__ = ga

foo.__setattr__ = sa




