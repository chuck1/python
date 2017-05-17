
import pylab as pl
import numpy as np

# f = focal length
def parab_y(x, f):
    return np.square(x) / 4.0 / f


x = np.linspace(-1,1,100)
y = parab_y(x, 0.5)

pl.plot(x,y)
pl.show()


