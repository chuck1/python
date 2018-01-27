import random
import math



class Route:
    speed = 1
    train_length = 1

    def __init__(self, edges):
        self.edges = edges
        self.windows = []

        for e in self.edges:
            e.route = self

        self.departures = []

    def time_to_point(self, p):
        t = 0
        
        for e in self.edges:
            t += e.length() / self.speed
            if e.p1 == p:
                break

        return t, t + self.train_length / self.speed

    def schedule(self, t):
        
        self.windows = sorted(self.windows, key=lambda w: w.t_0)

        for w in self.windows:
            if t <= w.t_0:
                break
            elif t < w.t_1:
                t = w.t_1
        
        p = self.edges[0].p0
        t_0, t_1 = self.time_to_point(p)
        p.reserve(t + t_0, t + t_1)

        for e in self.edges:
            t_0, t_1 = self.time_to_point(e.p1)
            e.p1.reserve(t + t_0, t + t_1)

        self.departures.append(t)

    def show(self):
        print('route')
        print('\twindows')
        for w in self.windows:
            print('\t\t{:8.1f} {:8.1f}'.format(w.t_0, w.t_1))
        print('\tdepartures')
        print('\t\t{}'.format(self.departures))

    def throughput(self):
        return len(self.departures) / max(self.departures)

    def plot(self, ax):
    
        X = [self.edges[0].p0.position[0]] + [e.p1.position[0] for e in self.edges]
        Y = [self.edges[0].p0.position[1]] + [e.p1.position[1] for e in self.edges]

        ax.plot(X, Y, '-o')



