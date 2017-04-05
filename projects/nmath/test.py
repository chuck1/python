#!/usr/bin/env python

import sys
import argparse
import sympy



def count_e(lst):
    c = 0
    for l in lst:
        if l[0] == 'e':
            c += 1
    return c

def mysort(lst):

    inverses = 0

    changed = True
    while changed:
        changed = False
    
        for i in range(len(lst)-1):
            s1 = lst[i]
            s2 = lst[i+1]
    
            if (s1[0]=='e') and (s2[0]=='e'):
    
                c = cmp(s1,s2)
    
                if c == 1:
                    lst[i] = s2
                    lst[i+1] = s1
                    inverses += 1
                    changed = True
    
    return inverses


def cancel(l, s):
    a = l.count(s)

    if a < 2: return

    b = a % 2

    for i in range(a-b):
        l.remove(s)

class cmp_functor(object):
    inverses = 0
    def __call__(self, x, y):
        if (x[0] == 'e') and (y[0] == 'e'):
            c = cmp(x,y)
            print "cmp({},{})={}".format(x,y,c)
    
            if c==-1:
                self.inverses += 1
    
            return c
    
        return 0


def cmp_symbol(x,y):
    if (x[0] == 'e') and (y[0] == 'e'):
        return 0

    if x[0] == 'e':
        return 1

    if y[0] == 'e':
        return -1

    return cmp(x,y)

def combin(lst, i1, d):
    for i2 in range(i1+1,d):
        lst2 = list(lst)
        lst2.append(i2)
        yield lst2
        for r in combin(lst2, i2, d): yield r

def even_subalg(d):
    c = list(combin(list(), -1, d))
    c = sorted(c, key=lambda x: len(x))
    c = [x for x in c if (len(x)%2)==0]
    return c

def b_coeff(x):
    #s = "b_{}".format("_".join([str(y+1) for y in x]))
    s = "b{}".format("".join([str(y+1) for y in x]))
    return s

def mul(lst):
    A = lst.pop(0)

    while lst:
        B = lst.pop(0)
        C = list()
        for a in A:
            for b in B:
                C.append(a+b)
        A = C

    return A

def process(lst):
    for e1 in lst:
        #inverses = 0
        
        #e2 = sorted(e1, cmp=cmp_symbol)

        f = cmp_functor()

        e2 = sorted(e1, cmp=cmp_symbol)
        #e3 = sorted(e2, cmp=f)
        e3 = list(e2)
        inv = mysort(e3)

        #e3 = ['-1']*(f.inverses % 2) + e3
        e3 = ['-1']*(inv % 2) + e3

        e4 = list(e3)
        cancel(e4, '-1')
        for x in basis:
            cancel(e4, x)

        #print "inverses={}".format(f.inverses)
        #print "inverses={}".format(inv)
        
        #print "{:36}={:36}={:36}={:36}".format(" ".join(e1)," ".join(e2)," ".join(e3)," ".join(e4))
        #print " ".join(e2)
        yield e4

def grades(E, gl):
    return [e for e in E if count_e(e) in gl]

def vector(s, d):
    coeff = [(s+"{}").format(i+1) for i in range(d)]
    basis = ["e{}".format(i+1) for i in range(d)]
    B = [[a,e] for a,e in zip(coeff,basis)]
    return B

def convert_add_mul(lst, dic):
    e = 0
    for x in lst:
        e += convert_mul(x, dic)
    return e

def convert_mul(lst, dic):
    e = 1
    for x in lst:
        e *= dic[x]
    return e

###########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("n", type=int)
args = parser.parse_args()

d=args.n

coeff = ["a{}".format(i+1) for i in range(d)]
basis = ["e{}".format(i+1) for i in range(d)]

print "coeff",coeff
print "basis",basis
print

c = even_subalg(d)
print "even combinations",len(c)
for x in c:
    print "  {}".format(x)

coeffs_b = ['b0'] + [b_coeff(x) for x in c]

syms_a = sympy.symbols(" ".join(coeff))
syms_b = sympy.symbols(" ".join(coeffs_b))
syms_e = sympy.symbols(" ".join(basis))
#print syms_b

sym_map = dict((x,y) for x,y in zip(coeffs_b + basis + coeff, syms_b + syms_e + syms_a))
sym_map['-1'] = -1
#print "map",sym_map
#print "coeffs_b", coeffs_b

Av1 = [[b_coeff(x)]+["e{}".format(t+1) for t in x] for x in c]
Av2 = [['-1']+x for x in Av1]
A1 = [['b0']] + Av1
A2 = [['b0']] + Av2

#print
#print "A1",A1
#print "A2",A2

#A = [['w'],['-1','x','e2','e3'],['-1','y','e3','e1'],['-1','z','e1','e2']]
#print "A",A

#B = [[a,e] for a,e in zip(coeff,basis)]
B = vector('a',d)

E0 = mul([A1, B, A2])

E = list(process(E0))

print


if 0:
    f = 0
    for e in E:
        #print e
        f += convert_mul(e, sym_map)
    print f

    sys.exit(0)

print "all terms   ", len(E)
E1 = [e for e in E if count_e(e) == 1]

print "vector terms", len(E1)

E2 = []
for s1 in basis:
    temp = []
    Etemp = [e for e in E1 if e[-1]==s1]
    [e.remove(s1) for e in Etemp]

    for s2 in coeff:
        temp2 = [e for e in Etemp if e.count(s2)]


        [e.remove(s2) for e in temp2]
        temp.append(temp2)

    print "terms", " ".join(["{:2}".format(len(x)) for x in temp])
    

    E2.append(temp)


if 1:
    print
    print
    for row in E2:
        for col in row:
            print "  "+" + ".join([" ".join(t) for t in col])
    
        fmt = "{:72}"*len(row)
        #print fmt.format(*[" + ".join([" ".join(t) for t in col]) for col in row])
        
        print


e2 = 0
E = list(process(mul([A1,A2])))
E = grades(E, [0])

for i in range(args.n+1):
    Etemp = grades(E, [i])
    print "grade={}".format(i)
    #print convert_add_mul(Etemp, sym_map)
    for e in Etemp:
        print "  {}".format(" ".join(e))
#sys.exit(0)

if 0:
    for x in E:
        print " ".join(x)
    sys.exit(0)

for x in E:
    #print x

    e = 1
    for y in x:
        e *= sym_map[y]

    #print e

    e2 += e


print
print "R = ", convert_add_mul(A1, sym_map)
print
print "R R~ = ",e2
print

sys.exit(0)

n = args.n

v1 = vector('r',n)
v2 = vector('f',n)

for x in list(process(mul([v1,v2]))):
    print x




