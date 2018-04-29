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


def tile(g0, m, n, x=0, y=0):

    h = math.ceil(g0.height())
    w = math.ceil(g0.width())
    
    for i in range(m):
        for j in range(n):
            #g = copy.deepcopy(g0)
            g = copy.copy(g0)

            #s = [(g0.width() + x) * i, (g0.height() + y) * j]
            s = [(w + x) * i, (h + y) * j]
            
            #g.position = g0.position + s

            g.shift(s)

            yield g

class InserterDirection(enum.Enum):
    SOUTH = None
    EAST = 6
    NORTH = 4
    WEST = 2

class BlueprintBook:
    @classmethod
    def read(self, filename):
        with open(filename) as f:
            p = json.load(f)

        return BlueprintBook(p)

    def __init__(self, data):
        self.data = data
    
    def find_print(self, label):
        for b in self.data['blueprint_book']['blueprints']:
            if b['blueprint']['label'] == label:
                return Blueprint(b['blueprint'])

empty_blueprint = {
        'entities': []
        }

class Blueprint:
    @classmethod
    def read(self, filename):
        with open(filename) as f:
            p = json.load(f)

        return Blueprint(p['blueprint'])

    def __init__(self, name, data=empty_blueprint):
        self.name = name
        self.data = data
        self.entities = [Entity.from_dict(e) for e in self.data['entities']]
        self.entities = sorted(self.entities, key=lambda e: e.name())

    def show(self, indent=0):
        for e in self.entities:
            e.show(indent)

    def x_min(self):
        ret = 0
        for e in self.entities:
            if e.x_min < ret:
                ret = e.x_min
        return ret

    def x_max(self):
        ret = 0
        for e in self.entities:
            if e.x_max > ret:
                ret = e.x_max
        return ret
     
    def y_min_plot(self):
        ret = 0
        for e in self.entities:
            y = e.y_min_plot
            if y < ret:
                ret = y
        return ret

    def y_min(self):
        ret = 0
        for e in self.entities:
            if e.y_min < ret:
                ret = e.y_min
        return ret

    def y_max_plot(self):
        ret = 0
        for e in self.entities:
            y = e.y_max_plot
            if y > ret:
                ret = y
        return ret

    def y_max(self):
        ret = 0
        for e in self.entities:
            if e.y_max > ret:
                ret = e.y_max
        return ret

    def color_straight_rail(self, e):
        d = e.get('direction', 0)
        
        m = {
                0: [0,0,1],
                1: [0,1,0],
                2: [0,1,1],
                3: [1,0,0],
                4: [1,0,1],
                5: [1,1,0],
                6: [0,0,0.5],
                7: [0,0.5,0],
                }
        
        return m[d]

    def count_entities(self):
        c = 0
        for e in self.entities:
            c += e.count_entities()
        return c

    def plot(self):
        print('plot')
        print(self.width(), self.height_plot())
        
        h_img = int(self.height_plot()) + 2
        w_img = int(self.width()) + 2
        img = np.ones((h_img, w_img, 3))
        
        x0 = -(math.ceil(self.x_min()) - 1 - 0.5)
        y0 = -(math.ceil(self.y_min_plot()) - 1 - 0.5)
        
        names = []

        n = self.count_entities()
        i_iter = iter(range(n))

        for e in self.entities:
            
            #if e.data['name'] not in names:
            #    print(e.data['name'])
            #    names.append(e.data['name'])
            
            #progressbar.progress_bar(i, n)

            e.plot(img, np.array([x0, y0]), i_iter, n)
               
        fig = plt.figure()

        ax = fig.add_subplot(111)

        imgplot = ax.imshow(img)

        #loc = plticker.MultipleLocator(base=1)
        #ax.xaxis.set_major_locator(loc)
        #ax.yaxis.set_major_locator(loc)
        #ax.grid(which='major', axis='both', linestyle='-')
        
        mpimg.imsave(self.name + '.png', img)

        plt.show()

    def width(self):
        return self.x_max() - self.x_min() + 1

    def height(self):
        return self.y_max() - self.y_min() + 1

    def height_plot(self):
        return self.y_max_plot() - self.y_min_plot() + 1


   



