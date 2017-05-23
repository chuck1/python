#!/usr/bin/env python3

MAX_INDENT = 8

def explore(a, indent=0, p=False, stack=[]):
        try:
            if isinstance(a, str):
                if p:
                    print(' '*indent + repr(a))
                pass
            elif isinstance(a, dict):
                explore_dict(a, indent, p)
            elif isinstance(a, list):
                explore_list(a, indent)
            else:
                explore_obj(a, indent, p, stack)
        except Exception as e:
            #print(' '*indent + str(e))
            pass

def explore_dict(obj, indent=0, p=False):
    if indent > MAX_INDENT: return

    for name, v in obj.items():
        if p:
            print(' '*indent + str(name))
        explore(v, indent+2)

def explore_list(obj, indent=0):
    if indent > MAX_INDENT: return

    for v in obj:
        #print(' '*indent + str(v))
        explore(v, indent+2)

def explore_obj(obj, indent=0, p_=False, stack=[]):
    if indent > MAX_INDENT: return

    for name in dir(obj):

        p = p_
        if name in ('__globals__', '__builtins__',):
            print(' '*indent + str(name))
            print(s)
            p = True

        try:
            a = getattr(obj, name)
            if a in stack:
                explore('loop found.', indent+2, p)
            else:
                s = list(stack)
                s.append(name)
                s.append(a)
                explore(a, indent=indent+2, p=p, stack=s)
        except Exception as e:
            explore(str(e), indent+2, p)



class Foo(object):
    def __init__(self):
        self.a = 1
        self.b = 2

    def func1(self):
        print('func1')

    def __getattribute__(self, name):
        #if name in ('a',):
        if name in ('a', '__dict__', '__class__', 'func2'):
            return object.__getattribute__(self, name)
        else:
            return "get not allowed {}".format(name)

    def __setattr__(self, name, v):
        if name in ('a',):
            object.__setattr__(self, name, v)
        else:
            print("set not allowed {}".format(name))

g = {'__builtins__':{'print':print}}
exec('def func2(self):\n  print(self,\'a=\',self.a,\'b=\',self.b)\n', g)
Foo.func2 = g['func2']


class Bar(object):
    def __getattribute__(self, name):
        print('bar get',name)
        return object.__getattribute__(self, name)
    a = 1
    b = 2


bar = Bar()

foo = Foo()

print(foo.a)
print(foo.b)

def ga(self, name):
    return object.__getattribute__(self, name)
    
def sa(self, name, v):
    object.__setattr__(self, name, v)

foo.__getattribute__ = ga

foo.__setattr__ = sa

foo.__getattribute__ = ga

foo.__setattr__ = sa

print(foo.a)
print(foo.b)

print(foo.func2.__func__.__globals__)

explore(foo, stack=[foo])

