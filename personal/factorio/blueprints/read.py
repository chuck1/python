import math
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

with open(sys.argv[1]) as f:
    p = json.load(f)

def find_print(label):
    for b in p['blueprint_book']['blueprints']:
        if b['blueprint']['label'] == label:
            return b['blueprint']
 
for b in p['blueprint_book']['blueprints']:
    print(b['blueprint']['label'])

class Blueprint:
    def __init__(self, data):
        self.data = data

    def x_min(self):
        ret = 0
        for e in self.data['entities']:
            if e['position']['x'] < ret:
                ret = e['position']['x']
        return ret

    def x_max(self):
        ret = 0
        for e in self.data['entities']:
            if e['position']['x'] > ret:
                ret = e['position']['x']
        return ret
     
    def y_min(self):
        ret = 0
        for e in self.data['entities']:
            if e['position']['y'] < ret:
                ret = e['position']['y']
        return ret

    def y_max(self):
        ret = 0
        for e in self.data['entities']:
            if e['position']['y'] > ret:
                ret = e['position']['y']
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

    def entity_color(self, e):
        m = {
                'straight-rail': self.color_straight_rail,
                'curved-rail': [0.1,0.1,0.5],
                }
        if e['name'] in m:
            c = m[e['name']]

            if callable(c):
                c = c(e)

            return c

    def plot(self):
        img = np.ones((self.width(), self.height(), 3))
        
        x0 = self.x_min()
        y0 = self.y_min()
           
        names = []

        for e in self.data['entities']:
            
            if e['name'] not in names:
                print(e['name'])
                names.append(e['name'])
            
            c = self.entity_color(e)

            if c is None: continue

            #print(e)

            x = e['position']['x'] - x0
            y = e['position']['y'] - y0
            
            if (x % 1) == 0:
                X = [x]
            else:
                X = [math.floor(x), math.ceil(x)]

            if (y % 1) == 0:
                Y = [y]
            else:
                Y = [math.floor(y), math.ceil(y)]
            
            for x in X:
                for y in Y:
                    img[x, y] = c

        imgplot = plt.imshow(img)
        plt.show()

    def width(self):
        return self.x_max() - self.x_min() + 1

    def height(self):
        return self.y_max() - self.y_min() + 1

def show(b):
    b = Blueprint(b)

    #for e in b['entities']:
    #    print(e)

    b.plot()

show(find_print("4-way Junction"))

