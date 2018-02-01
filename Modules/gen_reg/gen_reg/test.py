#!/usr/bin/env python3
import gen_reg
import numpy
import matplotlib.pyplot as plt

def func(x,c):
    return c[0] * numpy.power(x[0],c[1]) * numpy.power(x[1], c[2] * numpy.power(x[0],c[3]))

def func_jac(x,c):
    y = c[0] * numpy.power(x[0],c[1]) * numpy.power(x[1], c[2] * numpy.power(x[0],c[3]))

    return [
        numpy.power(x[0],c[1]) * numpy.power(x[1], c[2] * numpy.power(x[0],c[3])),
        y * numpy.log(x[0]),
        y * numpy.log(x[1]) * numpy.power(x[0],c[3]),
        y * numpy.log(x[0]) * numpy.log(x[1]) * c[2] * numpy.power(x[0],c[3])]

def func_plot_x(x,c):
    return numpy.log(numpy.power(x[0],c[1]) * numpy.power(x[1], c[2] * numpy.power(x[0],c[3])))
    return numpy.log(numpy.power(x[1], numpy.power(x[0],c[3])))
    #return numpy.log(x[1])
    #return x[1]

def func_plot_y(y):
    return numpy.log(y)

c0 = numpy.array([4,2,0.1,1.5])

x = numpy.array([[1,1,1,2,2,2,3,3,3],[2,4,6,2,4,6,2,4,6]])

#y = numpy.array([1,4,9,16,25,36])
y = func(x,c0)

c = [1,1,1,1]

print('x[0]',x[0])
print('x[1]',x[1])
print('y   ',y)
print('c   ',c)

res = gen_reg.fit(func, x, y, c, func_jac)
c = res.x

print('c',c)
print('c0',c0)

plt.plot(func_plot_x(x,c0), func_plot_y(y), 'o')
plt.plot(func_plot_x(x,c), func_plot_y(y), 'o')

plt.show()

