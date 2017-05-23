
def try_eval(s, g=None):
    print('------------------')
    print(s)
    print()
    try:
        r = eval(s, g)
    except Exception as e:
        print(e)
    else:
        print(r)
    print('------------------')


def func():
    print('func has been called')
    print(open)

class Foo(object):
    def func(self):
        print('Foo func has been called')
        print(open)

try_eval('func.__globals__.keys()')

try_eval('func.__globals__[\'__builtins__\']')


foo = Foo()

print(foo.func.__func__)
print(dir(foo.func))
print(dir(foo.func.__func__))
print(foo.func.__func__.__globals__)
print(foo.func.__func__.__globals__['__builtins__'])

func.__globals__['__builtins__'] = None

foo.func()

try:
    print(foo.func.__globals__['__builtins__'].open)
except Exception as e:
    print(e)

print('----------')

print(dir(Foo))
print(dir(Foo))




