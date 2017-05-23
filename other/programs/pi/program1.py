import fractions
import math
import sys

def step(a, b, n):
    c = fractions.gcd(b, n**2)
    
    d = n**2 / c
    e = b / c
    
    return a * d + e, b * d

    #return (a * n**2 + b), (b * n**2)

a = 1
b = 1

print math.pi**2/6.0
sys.exit(0)

for i in range(2,10000):
    #print a,b
    #print i, math.sqrt(6.0 * float(a)/b)

    print
    print a
    print b
    print a % b
    print (a-(a%b))/b

    print float(a)/b

    a,b = step(a,b,i)




