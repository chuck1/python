import functools
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

from .event import *

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

    def train_position_plots(self, ax):
        
        #plots = []
        
        for route in self.routes:
            for s in route.schedules:
                t_0, t_1 = s.edge_window(self)

                plot = TrainPositionPlot([t_0, t_1], [0, 1])
                plot.plot(ax)
                #plots.append()

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

