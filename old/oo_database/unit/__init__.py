

class Node:
    def __add__(self, r):
        return Add(self, r)
    
    def __sub__(self, r):
        return Sub(self, r)
    
    def __mul__(self, r):
        return Mul(self, r)

    def resolve(self):
        return self

class Single:
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return str(self.v)

    def __eq__(self, r):
        return r == self.v
    
    def __add__(self, r):
        return Add(self.v, r)
    
    def __sub__(self, r):
        return Sub(self.v, r)
    
    def __mul__(self, r):
        return Mul(self.v, r)

    def resolve(self):
        return self.v

class Equal(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0} = {1})".format(self.l,self.r)

    def resolve(self):
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return l == r
        except:
            return Equal(l,r)

class Add(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0} + {1})".format(self.l,self.r)

    def resolve(self):
        print('Add.resolve')
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return Single(l + r)
        except:
            return Add(l,r)

class Sub(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0} - {1})".format(self.l,self.r)

    def resolve(self):
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r

        try:
            return Single(l - r)
        except:
            return Sub(l,r)

class Mul(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0}*{1})".format(self.l,self.r)

    def resolve(self):
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return Single(l * r)
        except:
            return Mul(l,r)

    def ldist(self):
        if not (type(self.l) is Add or type(self.l) is Sub or type(self.l) is Equal):
            return None
        
        l = Mul(self.l.l, self.r)
        r = Mul(self.l.r, self.r)
        return type(self.l)(l,r)

class Div(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0}/{1})".format(self.l,self.r)

    def resolve(self):
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return Single(l / r)
        except:
            return Div(l,r)


class Pow(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0}^{1})".format(self.l,self.r)

    def resolve(self):
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return Single(l**r)
        except:
            return Pow(l,r)


#####################################

class Unit:

    def __eq__(self, r):
        return type(self) == type(r)

    def __add__(self, r):
        print('Unit.add')
        print(type(self))
        print(type(r))
        if self == r:
            return type(self)()
        else:
            print('error')
            raise 0

class Meter(Unit):
    def __str__(self):
        return 'm'

class Gram(Unit):
    def __str__(self):
        return 'g'

class Kilogram(Unit):
    def __str__(self):
        return 'kg'

class Second(Unit):
    def __str__(self):
        return 's'

#####################################


class Value:
    def __init__(self, v, u):
        self.v = v
        if isinstance(u, Node):
            self.u = u.resolve()
        else:
            self.u = Single(u)

        print(type(self.u))

    def __add__(self, r):
        if isinstance(r, Value):
            return Value(
                self.v + r.v,
                self.u + r.u)
        else:
            raise 0
        
    def __sub__(self, r):
        if isinstance(r, Value):
            return Value(
                self.v - r.v,
                self.u - r.u)
        else:
            raise 0
    
    def __mul__(self, r):
        if isinstance(r, Value):
            return Value(
                self.v * r.v,
                self.u * r.u)
        else:
            raise 0
    
    def __str__(self):
        return "{0} {1}".format(str(self.v), str(self.u))

####################################

def test0():

    u0 = Single(Meter())

    u1 = Single(Meter())

    u0 += Meter()

    u0 = u0.resolve()

    print(u0)
    print(u1)

    print(u0 == u1)

def test1():

    v0 = Value(1.0, Meter())
    v1 = Value(1.0, Meter())
    
    print(v0+v1)

def test2():

    v0 = Value(1.0, Div(Kilogram(),Second()))

    print(v0)

# test    
if __name__ == '__main__':

    test2()









    
