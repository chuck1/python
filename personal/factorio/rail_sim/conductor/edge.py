import functools
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

from .event import *
from .edge_window import *

class Edges:
    edges = []
    
    @classmethod
    def edge(self, p0, p1):
        for e in self.edges:
            if e.p0 == p0 and e.p1 == p1:
                return e
        e = Edge(p0, p1)
        self.edges.append(e)
        return e

    @classmethod
    def plot(self, ax):

        o = 0

        for i, e in zip(range(len(self.edges)), self.edges):
            
            #for w, y in zip(p.reserved0, repeat([-.1, .1])):
            #    ax.plot([w.t_0, w.t_1], [i + y] * 2, '-o')

            x, y = e.occupancy()

            ax.plot([min(x)] * 2, [i * o] * 2, 'k', linewidth=.5)
            ax.plot([min(x)] * 2, [i * o + 1] * 2, 'k', linewidth=.5)

            y = np.array(y)
            ax.plot(x, y + i * o, label="edge [{:8.2f} {:8.2f}] -> [{:8.2f} {:8.2f}]".format(e.p0.position[0], e.p0.position[1], e.p1.position[0], e.p1.position[1]))


class TrainPositionPlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plot(self, ax):
        ax.plot(self.x, self.y)


class Edge:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        
        self.p0.edges.append(self)
        self.p1.edges.append(self)

        self.routes = []

    def length(self):
        x = self.p1.position[0] - self.p0.position[0]
        y = self.p1.position[1] - self.p0.position[1]
        return math.sqrt(x*x + y*y)

    def windows(self):
        for route in self.routes:
            for s in route.schedules:
                yield s.edge_window(self)

    def check_window(self, w0):
        
        for w in self.windows():
            if w == w0:
                continue
            
            if w0.t_0 < w.t_0:
                w1, w2 = w0, w
            else:
                w1, w2 = w, w0

            print("check window")
            print("w1.t_0 {:8.2f} w2.t_0 {:8.2f}".format(w1.t_0, w2.t_0))
            
            # w1 enters first so change w1 to the back of the train
            t = w1.schedule.route.train_length /  w1.schedule.edge_speed(w1.edge)
            w1 = w1 + t

            if w1.t_0 > w2.t_0:
                print("{:8} > {:8}".format("w1.t_0", "w2.t_0"))
                print("{:8.2f} > {:8.2f}".format(w1.t_0, w2.t_0))
                return False

            if w1.t_1 > w2.t_1:
                print("{:8} > {:8}".format("w1.t_1", "w2.t_1"))
                print("{:8.2f} > {:8.2f}".format(w1.t_1, w2.t_1))
                return False
        
        return True

    def train_position_plots(self, ax):
        
        windows = list(self.windows())

        for w in windows:

            if self.check_window(w):
                continue
            
            print('would plot')
            continue

            plot = TrainPositionPlot([w.t_0, w.t_1], [0, 1])
            plot.plot(ax)

    def occupancy(self):
    
        events = []
        
        for w in self.p0.reserved0:
            if w.edge1 == self:
                events.append(Event(w.t_0, 1))

        for w in self.p1.reserved0:
            if w.edge0 == self:
                events.append(Event(w.t_1, -1))

        events = sorted(events, key=lambda e: e.t)

        x = [0]
        y = [0]

        for e in events:
            x.append(e.t)
            y.append(y[-1])

            x.append(e.t)
            y.append(y[-1] + e.y)

        return x, y

