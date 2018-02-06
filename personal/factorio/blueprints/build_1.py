import copy
import enum
import fractions

from .templates import *
from .blueprint import *

def tile_gap(g0, m, n, w_x, w_y, x=0, y=0):
    for i in range(m):
        for j in range(n):
            g = copy.deepcopy(g0)
            
            if i >= m / 2:
                x1 = w_x
            else:
                x1 = 0

            if j >= n / 2:
                y1 = w_y
            else:
                y1 = 0

            s = [(g0.width() + x) * i + x1, (g0.height() + y) * j + y1]
            g.shift(s)
            yield g

def gcd(X):
    X = list(X)
    ret = X.pop()
    for x in X:
        ret = fractions.gcd(ret, x)
    return ret

def distribute(counts_and_blueprints):

    counts_and_blueprints = [x for x in counts_and_blueprints if x[0] > 0]
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

def add_beacons_north(b):
    x0 = b.x_min()
    y0 = b.y_min()
    n = int((b.width() - 4) // 6)

    for i in range(n):
        b.entities.append(Entity({'name':'beacon'}, [x0 + 1 + 3 * (i + 0) + 0, y0 - 2]))
    
    for i in range(n):
        b.entities.append(Entity({'name':'beacon'}, [x0 + 1 + 3 * (i + n) + 4, y0 - 2]))

def layout_y(generator):
    l = []

    for b in generator:
        if l:
            sy = l[-1].y_max() - b.y_min() + 1
            b.shift([0, sy])
        l.append(b)
    
    return Group(l)

def stops_in_middle(g0, stops, stop_blueprints, m, n):

    g1 = Group(tile_gap(g0, n, 1, 4, 0))
    
    l = []
    
    m1 = m // 2
    m2 = m - m1

    for b in stop_blueprints:
        s = [math.ceil(g1.center()[0] - b.center()[0]), 0]
        b.shift(s)


    for i in range(m1):
        b1 = copy.deepcopy(g1)

        if i == 0:
            add_beacons_north(b1)
        
        yield b1
        
    for c, b in zip(stops, stop_blueprints):
        for i in range(int(c)):
            b1 = copy.deepcopy(b)
            yield b1

    for i in range(m2):
        b1 = copy.deepcopy(g1)

        if i == 0:
            add_beacons_north(b1)
        
        yield b1
 
def stops_distributed(g0, stops, stop_blueprints, m, n):

    g1 = Group(tile(g0, 1, n))
    
    l = []
    
    stop_blueprints = [repeat(b) for b in stop_blueprints]

    stops_1 = list(distribute(zip(stops, stop_blueprints)))
    for b in stops_1:
        s = [0, math.ceil(g1.center()[1] - b.center()[1])]
        b.shift()
    
    blueprints = distribute([(len(stops_1), iter(stops_1)), (m, repeat(g1))])

    for b in blueprints:
        b1 = copy.deepcopy(b)

        if l:
            b1.shift([l[-1].x_max() - b1.x_min() + 1, 0])

        l.append(b1)

    return Group(l)

def subfactory(g0, stops, stop_blueprints, m, n):
    g = layout_y(stops_in_middle(g0, stops, stop_blueprints, m, n))

    h = g.height()

    for g1 in g.entities:
        if isinstance(g1, GroupTrainStop):
            pass

    return g

if __name__ == '__main__':

    g = subfactory(assembling(), [3, 7], [train_stop(8, .4), train_stop(8, .4)], 4, 1)

    b = Blueprint()

    b.entities.append(g)
    
    b.plot()



