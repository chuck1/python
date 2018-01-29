import random
import math
import numpy as np
from conductor.route import *
import matplotlib.pyplot as plt

speed = 1
train_length = 1

class Window:
    def __init__(self, t_0, t_1):
        self.t_0 = t_0
        self.t_1 = t_1

class Point:
    def __init__(self, position):
        self.position = position
        
        self.edges = []

        self.reserved = []

    def reserve(self, t_0, t_1):

        self.reserved.append(Window(t_0, t_1))

        for e in self.edges:
            T_0, T_1 = e.route.time_to_point(self)
            e.route.windows.append(Window(t_0 - T_1, t_1 - T_0))

def repeat(S):
    while True:
        for s in S:
            yield s

class Points:
    def __init__(self, routes):

        self.points = []

        for r in routes:
            for p in r.points():
                if p not in self.points:
                    self.points.append(p)

    def plot(self, ax):
        
        for i, p in zip(range(len(self.points)), self.points):
            for w, y in zip(p.reserved, repeat([-.1, .1])):
                ax.plot([w.t_0, w.t_1], [i + y] * 2, '-o')


class Edge:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

        self.p0.edges.append(self)
        self.p1.edges.append(self)

    def length(self):
        x = self.p1.position[0] - self.p0.position[0]
        y = self.p1.position[1] - self.p0.position[1]
        return math.sqrt(x*x + y*y)

def edges(points):
    return [Edge(p0, p1) for p0, p1 in zip(points[:-1], points[1:])]

def route(points, indices=None):
    if indices is None:
        p = points
    else:
        p = [points[i] for i in indices]

    return Route([Edge(p0, p1) for p0, p1 in zip(p[:-1], p[1:])])

def test_1(n):
    print('single rail')
    points = [
            Point([0,0]),
            Point([2,0]),
            ]

    routes = [
            route(points, [0, 1]),
            ]

    
    r0 = routes[0]

    for i in range(n):
        for r in routes:
            r.schedule(0)

    show_routes(routes)
    plot_routes(routes)

def show_routes(routes):
    print('routes')
    t = 0
    for r in routes:
        #r.show()
        t1 = r.throughput()
        print('\t{:4} {:8.2f}'.format(len(r.departures), t1))
        t += t1

    print('{:8.2f}'.format(t))

def test_2(n):
    print('simple crossing')
    points = [
            Point([-2, 0]),
            Point([0, -2]),
            Point([0, 0]),
            ]

    routes = [
            route(points, [0, 2]),
            route(points, [1, 2]),
            ]

    
    r0 = routes[0]
    r1 = routes[1]

    for i in range(n):
        for r in routes:
            r.schedule(0)

    show_routes(routes)

def test_3(n):
    points = [
            Point([-2, 0]),
            Point([-1, 0]),
            Point([0, -2]),
            Point([0, -1]),
            Point([0, 0]),
            Point([1, 0]),
            Point([2, 0]),
            Point([0, 1]),
            Point([0, 2]),
            ]

    routes = [
            route(points, [0, 1, 4, 5, 6]),
            route(points, [0, 1, 4, 7, 8]),
            route(points, [2, 3, 4, 5, 6]),
            route(points, [2, 3, 4, 7, 8]),
            ]

    
    r0 = routes[0]
    r1 = routes[1]

    for i in range(n):
        for r in routes:
            r.schedule(0)

    show_routes(routes)

def random_arrivals(routes, n):
    for i in range(n):
        for j in range(len(routes)):
            k = random.randrange(len(routes))
            print('schdule route', k)
            routes[k].schedule(0)

def test_4(n):
    points = [
            Point([-2, 0]),
            Point([-1, 0]),
            Point([0, -2]),
            Point([0, -1]),
            Point([0, 0]),
            Point([1, 0]),
            Point([2, 0]),
            Point([0, 1]),
            Point([0, 2]),
            ]

    routes = [
            route(points, [0, 1, 4, 5, 6]),
            route(points, [0, 1, 7, 8]),
            route(points, [2, 3, 5, 6]),
            route(points, [2, 3, 4, 7, 8]),
            ]

    
    random_arrivals(routes, n)
    show_routes(routes)

def slope(p0, p1):
    return (p1.position[1] - p0.position[1]) / (p1.position[0] - p0.position[0])

def intercept(p0, p1):
    m = slope(p0, p1)
    return p0.position[1] - m * p0.position[0]

def intersection(p0, p1, q0, q1):
    m1 = slope(p0, p1)
    m2 = slope(q0, q1)
    b1 = intercept(p0, p1)
    b2 = intercept(q0, q1)
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return [x, y]

def merge_bus_0(n):

    points0 = [Point([0, y]) for y in range(n)]
    points1 = [Point([0, y + n]) for y in range(n)]

    points2 = [Point([n, y + n/2]) for y in range(n)]

    point_merge = Point([n/2, n + 0.5])

    edges0 = []
    edges1 = []

    for i in range(n):
        P = [points0[i], point_merge, points2[i]]
        edges0.append(edges(P))

    for i in range(n):
        P = [points1[i], point_merge, points2[i]]
        edges1.append(edges(P))

    return points0, points1, points2, edges0, edges1

def crossing_grid(n):
    for i in range(n):
        yield [None]*n

def merge_bus_2(n, points0, points1, o, d=1):
    o = np.array(o)

    pl0 = []
    pl1 = []

    points2 = [Point((o + [n, y + n/2]) * d) for y in range(n)]
    
    crossing_points = list(crossing_grid(n))
 
    for i in range(n):
        for j in range(i):
            p = Point(intersection(points0[i], points2[i], points1[j], points2[j]))
            crossing_points[i][j] = p
            #crossing_points[j][i] = p
   
    for i in range(n):
        P = [points0[i]]

        for j in range(n):
            p = crossing_points[i][j]
            if p is not None:
                P.append(p)

        P.append(points2[i])
    
        pl0.append(P)

    for i in range(n):
        P = [points1[i]]

        for j in range(n - 1, i, -1):
            p = crossing_points[j][i]
            if p is not None:
                P.append(p)

        P.append(points2[i])
    
        pl1.append(P)

    return points2, pl0, pl1

def merge_bus_1(n, o, d=1):
    o = np.array(o)

    points0 = [Point((o + [0, y]) * d) for y in range(n)]
    points1 = [Point((o + [0, y + n]) * d) for y in range(n)]
    
    points2, pl0, pl1 = merge_bus_2(n, points0, points1, o, d)

    return points0, points1, points2, pl0, pl1

def test_5(n, a):
    print('merge bus single point')
    points0, points1, points2, edges0, edges1 = merge_bus_0(a)
    
    routes = [Route(edges) for edges in edges0 + edges1]

    random_arrivals(routes, n)
    show_routes(routes)

def two_to_bus(n, o, d=1):
    o = np.array(o)

    points0, points1, points2, pl0, pl1 = merge_bus_1(n, o, d)
 
    point0 = Point((o + [-n, ((n - 1) / 2)]) * d)
    point1 = Point((o + [-n, ((n - 1) / 2 + n)]) * d)
    
    for pl in pl0:
        pl.insert(0, point0)

    for pl in pl1:
        pl.insert(0, point1)

    return points2, pl0, pl1

def test_6a(n, a):
    print('merge bus')

    points0, points1, points2, pl0, pl1 = merge_bus_1(a, [0,0])
 
    routes = [Route(edges(pl)) for pl in pl0] + [Route(edges(pl)) for pl in pl1]

    random_arrivals(routes, n)
    show_routes(routes)
    plot_routes(routes)

def test_6(n, a, train_length=1, d=1):
    print('merge bus')
    #points0, points1, points2, pl0, pl1 = merge_bus_1(a, [0,0])
 
    #point0 = Point([-a, (a - 1) / 2])
    #point1 = Point([-a, (a - 1) / 2 + a])
    
    points2, pl0, pl1 = two_to_bus(a, [0, 10], d)

    #routes = [Route(edges([point0] + pl)) for pl in pl0] + [Route(edges([point1] + pl)) for pl in pl1]
    routes = [Route(edges(pl), train_length) for pl in pl0] + [Route(edges(pl), train_length) for pl in pl1]

    random_arrivals(routes, n)
    show_routes(routes)
    plot_routes(routes)

def test_7_routes(samples, n):

    points_a, a0, a1 = two_to_bus(n, [0, 0])
    points_b, b0, b1 = two_to_bus(n, [0, 2*n])

    points_2, pl0, pl1 = merge_bus_2(n, points_a, points_b, [2*n, 0])

    for pl_a in [a0, a1]:
        for c, d in zip(pl_a, pl0):
            z = c + d[1:]
            yield z

    for pl_b in [b0, b1]:
        for c, d in zip(pl_b, pl1):
            z = c + d[1:]
            yield z

def plot_routes(routes):
    fig = plt.figure()
    ax = fig.add_subplot(121)

    for r in routes:
        r.plot(ax)
    
    ax = fig.add_subplot(122)

    Points(routes).plot(ax)

    plt.show()

def test_7(samples, n):
    routes = [Route(edges(pl)) for pl in test_7_routes(samples, n)]
    random_arrivals(routes, samples)
    show_routes(routes)
    plot_routes(routes)

def crossing(n):
    points_a0 = [Point([0, i]) for i in range(n)]
    points_a1 = [Point([n, i + n]) for i in range(n)]

    points_b0 = [Point([0, i + n]) for i in range(n)]
    points_b1 = [Point([n, i]) for i in range(n)]
    
    
    crossing_points = list(crossing_grid(n))

    for i in range(n):
        for j in range(n):
            crossing_points[i][j] = Point(intersection(points_a0[i], points_a1[i], points_b0[j], points_b1[j]))

    pl_a = []
    pl_b = []

    for i in range(n):
        P = [points_a0[i]]

        for j in range(n):
            p = crossing_points[i][j]
            if p is not None:
                P.append(p)

        P.append(points_a1[i])
    
        pl_a.append(P)

    for i in range(n):
        P = [points_b0[i]]

        for j in range(n - 1, -1, -1):
            p = crossing_points[j][i]
            if p is not None:
                P.append(p)

        P.append(points_b1[i])
    
        pl_b.append(P)

    return pl_a, pl_b


def test_crossing(samples, n):
    pl0, pl1 = crossing(n)
    
    print(pl0)
    print(pl1)

    routes = [Route(edges(pl)) for pl in pl0] + [Route(edges(pl)) for pl in pl1]

    random_arrivals(routes, samples)
    show_routes(routes)
    plot_routes(routes)



def test_crossing_1():
    test_crossing(100, 1)
    test_crossing(100, 2)
    test_crossing(100, 3)
    test_crossing(100, 4)

if __name__ == '__main__':
    
    #test_1(10)
    #test_2(100)
    #test_3(100)
    #test_4(100)
    #test_5(100, 2)
    #test_6a(100, 4)
    test_6(10, 4, train_length=1, d=1)
    #test_7(100, 4)
    
    #test_crossing(10, 2)



