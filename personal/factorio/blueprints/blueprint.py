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

def tile(g0, m, n, x=0, y=0):

    h = math.ceil(g0.height())
    w = math.ceil(g0.width())
    
    for i in range(m):
        for j in range(n):
            g = copy.deepcopy(g0)
            #s = [(g0.width() + x) * i, (g0.height() + y) * j]
            s = [(w + x) * i, (h + y) * j]
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

class Group:
    def __init__(self, entities):
        self.entities = list(entities)
        
        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

    def include_all(self):
        self.y_min_exclude = False
        self.y_max_exclude = False
        self.x_min_exclude = False
        self.x_max_exclude = False

        for e in self.entities:
            e.include_all()

    def name(self):
        return 'group'

    def plot(self, img, x0, y0):
        for e in self.entities:
            e.plot(img, x0, y0)

    def shift(self, p):
        for e in self.entities:
            e.shift(p)

    def x_min(self):
        ret = float("inf")
        for e in self.entities:
            if e.x_min() < ret:
                ret = e.x_min()
        return ret

    def x_max(self):
        ret = -float("inf")
        for e in self.entities:
            if e.x_max() > ret:
                ret = e.x_max()
        return ret
     
    def y_min_plot(self):
        ret = float("inf")
        for e in self.entities:
            y = e.y_min_plot()
            if y < ret:
                ret = y
        return ret

    def y_min(self):
        ret = float("inf")

        if self.y_min_exclude:
            return ret

        for e in self.entities:
            y = e.y_min()
            if y < ret:
                ret = y
        return ret

    def y_max(self):
        ret = -float("inf")
        
        if self.y_max_exclude:
            return ret

        for e in self.entities:
            y = e.y_max()
            if y > ret:
                ret = y
        return ret

    def width(self):
        return self.x_max() - self.x_min() + 1

    def height(self):
        return self.y_max() - self.y_min() + 1

    def height_plot(self):
        return self.y_max() - self.y_min_plot() + 1

    def center(self):
        return np.array([
                (self.x_max() + self.x_min()) / 2,
                (self.y_max() + self.y_min()) / 2,
                ])

    def show(self, indent=0):
        print(' ' * indent + 'group')
        for e in self.entities:
            e.show(indent + 1)

class Entity:
    @classmethod
    def from_dict(self, data):
        p = np.array([data['position']['x'], data['position']['y']])
        return Entity(data, p)

    def __init__(self, data, position):
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

    def x_min(self):
        ret = self.position[0] - (self.footprint()[0] - 1) / 2
        return ret

    def x_max(self):
        return self.position[0] + (self.footprint()[0] - 1) / 2

    def y_min(self):
        if self.y_min_exclude: return float('inf')
        return self.position[1] - (self.footprint()[1] - 1) / 2

    y_min_plot = y_min

    def y_max(self):
        return self.position[1] + (self.footprint()[1] - 1) / 2

    def width(self):
        return self.x_max() - self.x_min() + 1

    def height(self):
        return self.y_max() - self.y_min() + 1

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

    def plot(self, img, x0, y0):
        x = self.position[0] - x0
        y = self.position[1] - y0
        
        f = self.footprint()
        

        X = np.arange(x - (f[0] - 1) / 2, x + (f[0] + 1) / 2)
        Y = np.arange(y - (f[1] - 1) / 2, y + (f[1] + 1) / 2)

        #print(self.name(), f, x, y, X, Y)

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


empty_blueprint = {
        'entities': []
        }

class Blueprint:
    @classmethod
    def read(self, filename):
        with open(filename) as f:
            p = json.load(f)

        return Blueprint(p['blueprint'])

    def __init__(self, data=empty_blueprint):
        self.data = data
        self.entities = [Entity.from_dict(e) for e in self.data['entities']]
        self.entities = sorted(self.entities, key=lambda e: e.name())

    def show(self, indent=0):
        for e in self.entities:
            e.show(indent)

    def x_min(self):
        ret = 0
        for e in self.entities:
            if e.x_min() < ret:
                ret = e.x_min()
        return ret

    def x_max(self):
        ret = 0
        for e in self.entities:
            if e.x_max() > ret:
                ret = e.x_max()
        return ret
     
    def y_min_plot(self):
        ret = 0
        for e in self.entities:
            y = e.y_min_plot()
            if y < ret:
                ret = y
        return ret

    def y_min(self):
        ret = 0
        for e in self.entities:
            if e.y_min() < ret:
                ret = e.y_min()
        return ret

    def y_max(self):
        ret = 0
        for e in self.entities:
            if e.y_max() > ret:
                ret = e.y_max()
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


    def plot(self):
        print('plot')
        print(self.width(), self.height_plot())
        
        h_img = int(self.height_plot()) + 2
        w_img = int(self.width()) + 2
        img = np.ones((h_img, w_img, 3))
        
        x0 = math.ceil(self.x_min()) - 1 - 0.5
        y0 = math.ceil(self.y_min_plot()) - 1 - 0.5
        
        names = []

        for e in self.entities:
            
            #if e.data['name'] not in names:
            #    print(e.data['name'])
            #    names.append(e.data['name'])
            
            e.plot(img, x0, y0)
               
        fig = plt.figure()

        ax = fig.add_subplot(111)

        imgplot = ax.imshow(img)

        #loc = plticker.MultipleLocator(base=1)
        #ax.xaxis.set_major_locator(loc)
        #ax.yaxis.set_major_locator(loc)
        #ax.grid(which='major', axis='both', linestyle='-')

        plt.show()

    def width(self):
        return self.x_max() - self.x_min() + 1

    def height(self):
        return self.y_max() - self.y_min() + 1

    def height_plot(self):
        return self.y_max() - self.y_min_plot() + 1



