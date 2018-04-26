import inspect

from CoolProp.CoolProp import PropsSI

class MyException(Exception): pass

class PointProperty:
    def __init__(self, s):
        self.s = s

    def calc(self, p):
        funcs = getattr(p, '_functions')
        
        if self.s not in funcs:
            funcs[self.s] = []

        for f in funcs[self.s]:
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

                #if getattr(p, '_volatile_' + self.s):
                #    delattr(p, '_' + self.s)
    
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

class PropertyClass:
    def __init__(self):
        self._stack = []
        self._functions = {}

class Point(PropertyClass):

    h = PointProperty('h')
    s = PointProperty('s')
    T = PointProperty('T')
    m = PointProperty('m')
    p = PointProperty('p')
    Q = PointProperty('Q')

    def __init__(self, i, f):
        super(Point, self).__init__()

        self.i = i
        self.f = f

        self._functions['p'] = []
        self._functions['h'] = [
                lambda p: PropsSI("H", "P", p.p, "Q", p.Q, p.f),
                lambda p: PropsSI("H", "P", p.p, "T", p.T, p.f),
                ]
        self._functions['s'] = [
                lambda p: PropsSI("S", "P", p.p, "H", p.h, p.f),
                lambda p: entropy_1(p),
                ]
        self._functions['T'] = [
                lambda p: PropsSI("T", "P", p.p, "H", p.h, p.f),
                lambda p: PropsSI("T", "P", p.p, "Q", p.Q, p.f),
                ]
        self._functions['m'] = [
                ]
        self._functions['Q'] = [
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


