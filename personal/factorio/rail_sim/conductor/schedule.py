import random
import math
import numpy as np

from .window import *
from .edge_window import *

DEBUG = False

"""
for implementing adjustable speed

store:
list of speeds corresponding to edges
start time
"""
class Schedule:
    def __init__(self, route, t_0):
        self.route = route
        self.t_0 = t_0
        self.speed = [self.route.speed] * len(self.route.edges)

    """
    return the entry and exit times for point p
    """
    def point_window(self, p0):

        t_0 = self.t_0

        if self.route.point_first() == p0:
            return Window(t_0, t_0 + self.route.train_length / self.route.speed, None, self.route.edges[0])

        for e, s in zip(self.route.edges, self.speed):
            p = e.p1

            t_0 += e.length() / s

            if p == p0:
                return Window(t_0, t_0 + self.route.train_length / self.route.speed, e, self.route.edge_next(e))
        
        raise RuntimeError()

    def edge_speed(self, edge):
        for e, s in zip(self.route.edges, self.speed):
            if e == edge:
                return s

    def edge_window(self, e):

        w0 = self.point_window(e.p0)
        w1 = self.point_window(e.p1)

        return EdgeWindow(e, self, w0.t_0, w1.t_0)

    def cleanup_points(self):
        """
        when a route creates a schedule, we know that when the route creates the next schedule
        the second schedule will have values of t_0 for each point greater than those for the first schedule
        """
        
        t_0 = self.point_window(self.route.point_first()).t_0
        
        for p in self.route.points():

            #w = self.point_window(p)
            
            #p.t_0[self.route] = w.t_0

            w = self.route.time_to_point(p)

            p.t_0[self.route] = t_0 + w.t_0

            p.cleanup()

    def width(self):
        t0 = self.point_window(self.route.point_first()).t_0
        t1 = self.point_window(self.route.point_last()).t_1
        return t1 - t0

    def find_conflict(self):

    for p in self.route.points_not_first()

    def find_conflict_point_not_first(self, p):
        
        W0 = self.point_window(p)

        for w in p.reserved:

            if W0.t_1 < w.t_0 + 1e-10:
                continue

            if W0.t_0 > w.t_1 - 1e-10:
                continue

            yield PointWindowConflict(self, W0, w)


