
class Node:
    def __add__(self, r):
        return Add(self, r)
    def __sub__(self, r):
        return Sub(self, r)
    def __mul__(self, r):
        return Mul(self, r)


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
        try:
            l = self.l.resolve()
        except:
            l = self.l

        try:
            r = self.r.resolve()
        except:
            r = self.r
        
        try:
            return l + r
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
            return l - r
        except:
            return Sub(l,r)

class Mul(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __str__(self):
        return "({0} * {1})".format(self.l,self.r)

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
            return l * r
        except:
            return Mul(l,r)

    def ldist(self):
        if not (type(self.l) is Add or type(self.l) is Sub or type(self.l) is Equal):
            return None
        
        l = Mul(self.l.l, self.r)
        r = Mul(self.l.r, self.r)
        return type(self.l)(l,r)


c = Add(1,2)

d = c * 4


print(d)

print(d.resolve())

print(d.ldist())
print(d.ldist().resolve())
