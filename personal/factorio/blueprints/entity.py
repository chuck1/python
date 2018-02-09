import math
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as plticker
import numpy as np
import enum
import copy
import progressbar

class EntityPosition:
    def __init__(self):
        pass
    def __get__(self, instance, owner):
        #print('get')
        #print(instance)
        #print(owner)
        return instance.__position
    def __set__(self, instance, value):
        #print('set')
        #print(instance)
        #print(value)
        instance.__position = value
        instance.invalidate()
    def __delete__(self, instance):
        print('delete')
        print(instance)

class Entity:
    position = EntityPosition()

    @classmethod
    def from_dict(self, data):
        p = np.array([data['position']['x'], data['position']['y']])
        return Entity(data, p)
    
    def invalidate(self):
        if self.group is not None:
            self.group.invalidate()

    def count_entities(self): return 1

    def __init__(self, data, position):
        self.group = None
        self.data = data
        self.position = np.array(position, dtype=float)
        
        f = self.footprint()
        
        #self.position[0] = self.position[0] - (f[0] - 1) / 2
        #self.position[1] -= (f[1] - 1) / 2
        
        #self.position += [0.5, 0.5]

        #print(self.name(), position, f, (f-1)/2, self.position)

        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

    def include_all(self):
        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

    def name(self):
        return self.data['name']

    def center(self):
        return self.position

    def color(self):
        m = {
                'straight-rail':            [0.0, 0.0, 0.0],#self.color_straight_rail,
                'curved-rail':              [1.0, 1.0, 0.0],
                'transport-belt':           [1.0, 1.0, 0.0],
                'assembling-machine-1':     [0.0, 0.0, 1.0],
                'inserter':                 [1.0, 0.5, 0.0],
                'passive-provider-chest':   [1.0, 0.0, 0.0],
                'requester-chest':          [0.0, 1.0, 0.0],
                'beacon':                   [0.5, 0.0, 0.0],
                'substation':               [0.2, 0.2, 0.5],
                'pipe':                     [1.0, 0.0, 1.0],
                'tank':                     [1.0, 0.0, 1.0],
                'pump':                     [1.0, 0.0, 1.0],
                }

        if self.data['name'] in m:
            c = m[self.data['name']]

            if callable(c):
                c = c(self)

            return c

    @property
    def x_min(self):
        ret = self.position[0] - (self.footprint()[0] - 1) / 2
        return ret

    @property
    def x_max(self):
        return self.position[0] + (self.footprint()[0] - 1) / 2

    @property
    def y_min(self):
        if self.y_min_exclude: return float('inf')
        return self.position[1] - (self.footprint()[1] - 1) / 2

    y_min_plot = y_min

    @property
    def y_max(self):
        if self.y_max_exclude: return float('-inf')
        return self.position[1] + (self.footprint()[1] - 1) / 2

    def width(self):
        return self.x_max - self.x_min + 1

    def height(self):
        return self.y_max - self.y_min + 1

    def shift(self, p):
        #print('shift', p)
        #print(self.position)
        self.position = self.position + np.array(p)
        #print(self.position)

    def footprint(self):
        footprints = {
                'assembling-machine-1': [3, 3],
                'beacon':               [3, 3],
                'substation':           [2, 2],
                'straight-rail':        [2, 2],
                'tank':                 [3, 3],
                'pump':                 [2, 1],
                }
        if self.data['name'] in footprints:
            return np.array(footprints[self.data['name']])

        return np.array([1, 1])

    def plot(self, img, x0, y0, i, n):
        x = self.position[0] - x0
        y = self.position[1] - y0
        
        f = self.footprint()

        X = np.arange(x - (f[0] - 1) / 2, x + (f[0] + 1) / 2)
        Y = np.arange(y - (f[1] - 1) / 2, y + (f[1] + 1) / 2)

        #print(self.name(), f, x, y, X, Y)

        progressbar.progress_bar(next(i), n)

        c = self.color()

        if c is None: return

        for x in X:
            for y in Y:
                x = int(round(x))
                y = int(round(y))
                
                blank = np.all(img[y, x] == np.array([1, 1, 1]))
                if blank or (self.name() == 'substation'):
                    img[y, x] = c

    def show(self, i=0):
        p = ' '*i
        print(p + '{:20}'.format(self.data['name']))
        for k, v in self.data.items():
            if k == 'name': continue
            print(' '*(i+1) + '{:16} {}'.format(k, v))




