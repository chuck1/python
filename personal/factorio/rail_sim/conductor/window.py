from .debug import *

class Window:

    tolerance = 1e-5

    def __init__(self, route, point, t_0, t_1):
        if t_0 > t_1:
            raise RuntimeError()
        
        self.route = route
        self.point = point
        
        self.t_0 = t_0
        self.t_1 = t_1

    def __add__(self, t):
        return Window(self.t_0 + t, self.t_1 + t)

    def edge0(self):
        return self.route.edge_before(self.point)

    def edge1(self):
        return self.route.edge_after(self.point)

    def check_conflict(self, w):
        if self.t_1 <= w.t_0 + self.tolerance:
            return False

        if w.t_1 <= self.t_0 + self.tolerance:
            return False
            
        if Debug.level >= 20:
            print('trying to reserve window  {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))
            print('but conflicts with window {:8.2f} {:8.2f}'.format(self.t_0, self.t_1))
            print(w.t_1 - self.t_0)
            print(self.t_1 - w.t_0)

        return True

    def plot(self, ax, x):
        ax.plot([self.t_0, self.t_1], [x] * 2, '-o')


