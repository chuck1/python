
class D:
    def __init__(self, f, *args):
        print('D __init__', f, args)
        self.f = f
    
    def __get__(self, obj, owner):
        print('D __get__', obj, owner)
        self.f(obj)

class A:

    def f(self):
        print('A f')

    d = D(f)

A.d

a = A()

a.d



