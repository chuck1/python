import math
import sympy
import numpy as np

def mul(a, b):
    return (
        a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
        a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
        a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
        a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],
        )

def angle_axis(a, v):
    return [
        math.cos(a / 2.),
        v[0] * math.sin(a / 2.),
        v[1] * math.sin(a / 2.),
        v[2] * math.sin(a / 2.),
        ]

def test():
    q = sympy.symbols('q0:4')
    b = sympy.symbols('b0:4')
    qc = (q[0], -q[1], -q[2], -q[3])
    
    bp = mul(mul(q,b),qc)[1:]

    for t in bp:
        print(sympy.expand(t))

def rotate(q, b):
    #q = sympy.symbols('q0:4')
    #b = sympy.symbols('b0:4')
    b = (0, b[0], b[1], b[2])
    qc = (q[0], -q[1], -q[2], -q[3])
    return mul(mul(q,b),qc)[1:]

class Example:
    def GetJ(self, x, o, v, b):
        #print('GetJ.', x, o, v, b)
        
        def f(j):
            return j(x, o, v, b)

        return np.vectorize(f)(self.J_lambda)

    def GetY(self, x, o, v, b):
        #print('GetJ.', x, o, v, b)
        
        def f(j):
            return j(x, o, v, b)

        return np.vectorize(f)(self.Y_lambda)

    def __init__(self):
        q = np.array(sympy.symbols('q0:4'))
        a = np.array(sympy.symbols('a0:3'))
        k = sympy.symbols('k0:4')
        o = np.array(sympy.symbols('o0:3'))
        v = [np.array(sympy.symbols('v_{}_0:3'.format(i))) for i in range(4)]
        b = [np.array(sympy.symbols('b_{}_0:3'.format(i))) for i in range(4)]

        self.Y = np.concatenate([(o + k[i] * v[i] - a - rotate(q, b[i])) for i in range(4)])
    
        #print(np.shape(y))
        #print(y)
        
        x = np.concatenate((q, a, k))

        self.lambda_args = (x, o, v, b)
        
        #print(x)
        
        self.J = np.array([[sympy.diff(y0,x0) for x0 in x] for y0 in self.Y])
    
        #print(np.shape(self.J))
    
        #print(self.J)
        
        def term(t):
            return sympy.lambdify(self.lambda_args, t)
        
        self.J_lambda = np.vectorize(term)(self.J)

        self.Y_lambda = np.vectorize(term)(self.Y)
    
def normalize(v):
    m = np.linalg.norm(v)
    return v / m

def x_from_parts(q, a, k):
    x = np.concatenate((q, np.reshape(a, (3,)), k))
    return x
    

def solve(f, fj, x, args):

    #while(True):
    for i in range(15):

        y = f(x, *args)
        
        print(" ".join("{:10.3e}".format(y1) for y1 in y))

        j = fj(x, *args)
        jt = np.transpose(j)
    
        ji = np.dot(np.linalg.inv(np.dot(jt, j)), jt)

        x = x - np.dot(ji, y)
        
def example():
    # create example o v b

    o = np.reshape(np.array([0.,0.,0.]), (3,1))
    a = np.reshape(np.array([0.,0.,1.]), (3,1))
    B = [
            np.reshape(np.array([0.,0.,0.]), (3,1)),
            np.reshape(np.array([1.,0.,0.]), (3,1)),
            np.reshape(np.array([0.,1.,0.]), (3,1)),
            np.reshape(np.array([0.,0.,1.]), (3,1)),
            ]
    
    q = angle_axis(math.pi/4, [0.,0.,1.])
    #q = angle_axis(0, [0,0,1])

    P = [(a + rotate(q, b)) for b in B]

    V1 = [(p - o) for p in P]

    for v1 in V1:
        print(v1)

    k = [np.linalg.norm(v) for v in V1]

    V = [normalize(v) for v in V1]

    x = np.concatenate((q, np.reshape(a, (3,)), k))

    if False:
        print(q,a,k)
    
        print('q')
        print(q)

        print('B')
        for b in B:
            print(b)
        
        print('P')
        for p in P:
            print(p)
        
        print('V')
        for v in V:
            print(v)

        print('x')
        print(x)

    return q, a, k, o, V, B

q, a, k, o, v, b = example()


e = Example()

#J = e.GetJ(x, o, v, b)

#print(J)

#Y = e.GetY(x, o, v, b)

#print(Y)

# perturb
a = np.array(a)
a[1,0] += 1.5

x = x_from_parts(q, a, k)

solve(e.GetY, e.GetJ, x, (o, v, b))







