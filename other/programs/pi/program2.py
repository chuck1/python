import math

def step(a,b):
    if (float(a)/float(b)) > math.pi:
        b += 1
    else:
        a += 1

    return a,b

a = 1
b = 1

for i in range(10000000):
    if (i % 100)==0:
        print i, a,b,float(a)/b
    a,b = step(a,b)




