


class Foo(object):
    def func1(self):
        print('func1')

def func2(self):
    print('func2')

Foo.func2 = func2

g = {'__builtins__': {'print': print}}
exec('def func3(self): print(\'func3\')', g)

Foo.func3 = g['func3']

foo=Foo()

foo.func1()
foo.func2()
foo.func3()

print(Foo.func1.__globals__['__builtins__'].open)
print(Foo.func2.__globals__['__builtins__'].open)
print(Foo.func3.__globals__['__builtins__'])






