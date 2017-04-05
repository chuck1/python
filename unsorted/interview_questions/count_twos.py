


def dumb(n):
    c = 0
    for i in xrange(n+1):
        d = str(i).count('2')
        #print i,d
        c += d
    return c

def smart(n):
    c = 0
    c +=      1*((n+8)//      10)
    c +=     10*((n+8)//     100)
    c +=    100*((n+0)//    1000)
    c +=   1000*((n+0)//   10000)
    c +=  10000*((n+0)//  100000)
    c += 100000*((n+0)// 1000000)
    return c

n = 10000
for i in xrange(n):
    print "{:8}{:8}{:8}".format(i, dumb(i), smart(i))

