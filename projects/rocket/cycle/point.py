import inspect

from CoolProp.CoolProp import PropsSI

class MyException(Exception): pass

class PointProperty:
    def __init__(self, s):
        self.s = s

    def calc(self, p):
        for f in getattr(p, '_functions_' + self.s):
            try:
                return f(p)
            except MyException as e:
                s = inspect.getsource(f)
                #print(f'{s!r} failed {e!r}')
                pass
        raise MyException()

    def __get__(self, p, owner):

        with PointContext(p, self.s):
            if hasattr(p, '_' + self.s):
        
                y = getattr(p, '_' + self.s)

                if getattr(p, '_volatile_' + self.s):
                    delattr(p, '_' + self.s)
    
                return y

            try:
                #with PointContext(p, self.s):
                y = self.calc(p)
                setattr(p, '_' + self.s, y)
                return y
    
            except MyException:
                pass

            if self.s in p._guess:
                return p._guess[self.s]
    
            raise MyException()

    def __set__(self, p, value):
        setattr(p, '_' + self.s, value)

class PointContext:
    def __init__(self, p, s):
        self.s = s
        self.p = p

    def __enter__(self):
        if self.s in self.p._stack:
            raise MyException()

        self.p._stack.append(self.s)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        
        self.p._stack.pop()
        

def entropy_1(p):
    p_sat = PropsSI("P", "T", p.T, "Q", 0, p.f)
    #print(p.p, p.T, p_sat)
    return PropsSI("S", "P", p.p, "T", p.T, p.f)

class Point:

    h = PointProperty('h')
    s = PointProperty('s')
    T = PointProperty('T')
    m = PointProperty('m')
    p = PointProperty('p')

    def __init__(self, i, f):
        self.i = i
        self.f = f
        self._stack = []

        self._functions_p = []
        self._functions_h = [
                lambda p: PropsSI("H", "P", p.p, "T", p.T, p.f),
                ]
        self._functions_s = [
                lambda p: PropsSI("S", "P", p.p, "H", p.h, p.f),
                lambda p: entropy_1(p),
                ]
        self._functions_T = [
                lambda p: PropsSI("T", "P", p.p, "H", p.h, p.f),
                ]
        self._functions_m = [
                ]

        self._volatile_p = False
        self._volatile_h = False
        self._volatile_s = False
        self._volatile_T = False
        self._volatile_m = False

        self._guess = {}

    def clear(self, s):
        if hasattr(self, '_' + s):
            delattr(self, '_' + s)

    def __str__(self):
        return f'point_{self.i}'


