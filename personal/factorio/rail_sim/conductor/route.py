import random
import math



class Route:
    speed = 1

    def __init__(self, edges, train_length=1):
        self.edges = edges
        self.windows = []
        self.train_length = train_length

        for e in self.edges:
            e.route = self

        self.departures = []

    def time_to_point(self, p):
        t = 0
        
        if p == self.edges[0].p0:
            return t, t + self.train_length / self.speed

        for e in self.edges:
            t += e.length() / self.speed
            if e.p1 == p:
                break

        return t, t + self.train_length / self.speed

    def check_point(self, p, t):
        t_0, t_1 = self.time_to_point(p)

        t_changed = False

        p.reserved = sorted(p.reserved, key=lambda w: w.t_0)
        
        print("check_point", p.position)
        if False:
            print('reserved')
            for w in p.reserved:
                print("\t{:8.2f} {:8.2f}".format(w.t_0, w.t_1))

        for w in p.reserved:
            T_0, T_1 = t_0 + t, t_1 + t
        
            if T_1 <= w.t_0:
                return t, t_changed
            elif T_0 < w.t_1:
                t = w.t_1 - t_0
                t_changed = True
        
        return t, t_changed

    def schedule(self, t):
        

        # find valid time
        
        t_changed = True
        while t_changed:
            for p in self.points():
                t, t_changed = self.check_point(p, t)
                if t_changed: break

        

        # reserve times in points

        for p in self.points():
            t_0, t_1 = self.time_to_point(p)
            p.reserve(t + t_0, t + t_1)

        self.departures.append(t)

    def points(self):
        yield self.edges[0].p0
        for e in self.edges:
            yield e.p1

    def show(self):
        print('route')
        print('\tpoints')
        for p in self.points():
            print('\t\t{:16} {:16}'.format(str(p.position), str(self.time_to_point(p))))
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



