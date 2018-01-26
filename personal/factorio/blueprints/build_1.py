import copy
import enum
import fractions

from templates import *
from .blueprint import *

def gcd(X):
    X = list(X)
    ret = X.pop()
    for x in X:
        ret = fractions.gcd(ret, x)
    return ret

def distribute(counts_and_blueprints):

    counts_and_blueprints = sorted(counts_and_blueprints, key=lambda x: x[0])
    
    s0, blueprints = zip(*counts_and_blueprints)
    
    g = int(gcd(s0))
    
    s0 = sorted(s0)
    
    s = np.array(s0)
    s1 = s / g

    x = int(min(s1))
    
    s2 = s1 // x
    r = np.mod(s1, x)

    print('g ', g)
    print('s ', s)
    print('s1', s1)
    print('x ', x)
    print('s2', s2)
    print('r ', r)
    
    for i in range(g):
        for y, b in zip(r, blueprints):
            for k in range(int(y)):
                yield next(b)

        for j in range(x):
            for y, b in zip(s2, blueprints):
                for k in range(int(y)):
                    yield next(b)

def repeat(b):
    while True:
        yield b
            
def subfactory(g0, stops, stop_blueprints, m, n):
    
    g1 = Group(tile(g0, 1, n))
    
    l = []
    
    stop_blueprints = [repeat(b) for b in stop_blueprints]

    stops_1 = list(distribute(zip(stops, stop_blueprints)))
    
    blueprints = distribute([(len(stops_1), iter(stops_1)), (m, repeat(g1))])

    for b in blueprints:
        b1 = copy.deepcopy(b)

        if l:
            b1.shift([l[-1].x_max() - b1.x_min() + 1, 0])

        l.append(b1)

    return Group(l)


if __name__ == '__main__':

    g = subfactory(assembling(), [3, 7], [train_stop(8, .4), train_stop(8, .4)], 4, 1)

    b = Blueprint()

    b.entities.append(g)

    b.plot()



