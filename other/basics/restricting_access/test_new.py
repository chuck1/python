

class Meta(type):
    def __new__(cls, name, bases, dct, **kwds):
        print(cls)
        print(name)
        print(bases)
        print(dct)
        print(**kwds)
        return type.__new__(cls, name, bases, dct, **kwds)

class Foo(object, metaclass=Meta):
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

class Bar(Foo, metaclass=type):
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

Foo()
Bar()

