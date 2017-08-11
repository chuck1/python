import datetime
import csv

import numpy as np
import matplotlib.pyplot as plt

def sub(y, l, n):
    for i in range(n):
        yield y[i:l-n+i+1]

def rolling(x, y, n):
    s = np.shape(y)
    l = s[0]
    m = 2 * n + 1
    
    X = x[n:l-n]
    Y = np.zeros(np.shape(X))

    for ys in sub(y, l, m):
        Y += ys
    Y /= m
    
    return X, Y

def read():
    with open('madras.txt') as f:
        reader = csv.reader(f)
        for row in reader:

            t = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M') - datetime.timedelta(hours=7)
            
            d = float(row[1]) / 60
        
            yield t, d

t, d = zip(*read())

plt.plot(t, d, 'o')

t1, d1 = rolling(t, d, 3)

plt.plot(t1, d1)
plt.show()

