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
from cached_property import cached_property

from .entity_position import *

class Group:
    position = EntityPosition()

    def __init__(self, entities):
        self.__entities = list(entities)

        self.position = np.zeros((2,))

        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

    def invalidate(self):

        if 'x_min' in self.__dict__:
            del self.__dict__['x_min']
        if 'x_max' in self.__dict__:
            del self.__dict__['x_max']
        if 'y_min' in self.__dict__:
            del self.__dict__['y_min']
        if 'y_min_plot' in self.__dict__:
            del self.__dict__['y_min_plot']
        if 'y_max' in self.__dict__:
            del self.__dict__['y_max']

    def include_all(self):
        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

        for e in self.entities:
            e.include_all()

    def count_entities(self):
        c = 0
        for e in self.entities:
            c += e.count_entities()
        return c

    @property
    def entities(self):
        for e in self.__entities:
            yield e
    
    def entities_append(self, e):
        self.__entities.append(e)
        self.invalidate()

    def name(self):
        return 'group'

    def plot(self, img, p0, i, n):
        for e in self.entities:
            e.plot(img, p0 + self.position, i, n)

    def shift(self, p):
        self.position = self.position + p
        #for e in self.entities:
        #    e.shift(p)

    @cached_property
    def x_min(self):
        ret = float("inf")
        for e in self.entities:
            x = e.x_min
            if x < ret:
                ret = x
        return ret + self.position[0]

    @cached_property
    def x_max(self):
        ret = -float("inf")
        for e in self.entities:
            x = e.x_max
            if x > ret:
                ret = x
        return ret + self.position[0]
     
    @cached_property
    def y_min_plot(self):
        ret = float("inf")
        for e in self.entities:
            y = e.y_min_plot
            if y < ret:
                ret = y
        return ret + self.position[1]

    @cached_property
    def y_min(self):
        ret = float("inf")

        if self.y_min_exclude:
            return ret

        for e in self.entities:
            y = e.y_min
            if y < ret:
                ret = y
        return ret + self.position[1]

    @cached_property
    def y_max_plot(self):
        ret = -float("inf")

        for e in self.entities:
            y = e.y_max_plot
            if y > ret:
                ret = y
        return ret + self.position[1]

    @cached_property
    def y_max(self):
        ret = -float("inf")
        
        if self.y_max_exclude:
            return ret

        for e in self.entities:
            y = e.y_max
            if y > ret:
                ret = y
        return ret + self.position[1]

    def width(self):
        return self.x_max - self.x_min + 1

    def height(self):
        return self.y_max - self.y_min + 1

    def height_plot(self):
        return self.y_max - self.y_min_plot + 1

    def center(self):
        return np.array([
                (self.x_max + self.x_min) / 2,
                (self.y_max + self.y_min) / 2,
                ])

    def show(self, indent=0):
        print(' ' * indent + 'group')
        for e in self.entities:
            e.show(indent + 1)


