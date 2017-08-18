
class Base(object):
    a = 0

class Foo(Base):
    pass

class Bar(Base):
    pass

print Base.a
print Foo.a
print Bar.a

Foo.a = 1

print Base.a
print Foo.a
print Bar.a

