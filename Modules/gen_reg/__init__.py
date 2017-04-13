
import scipy.optimize
import numpy

def op_func(c, f, x, y, j):
    y1 = f(x,c)
    e = numpy.sum(numpy.power(y1 - y,2))
    return e

"""
x - x from data points
y - y from data points
"""
def op_func_jac(c, f, x, y, j):
    y1 = f(x,c)
    dc = j(x,c)
    e0 = 2.0 * (y1 - y) * dc
    e1 = numpy.sum(e0,axis=1)
    #print('op_func_jac',numpy.shape(dc),numpy.shape(e0),numpy.shape(e1))
    return e1

"""
the function shall be of the form
y = f(x[0], x[1]...)

the x data shall be an array with m rows and n columns
where m is the number of inputs to the function
and n is the number of data points

the y data shall be an array with 1 row and n columns

"""
def fit(f, x, y, c, j=None):
    
    if False:
        for method in ['Nelder-Mead','Powell','CG','BFGS','Newton-CG','L-BFGS-B','TNC','COBLYA','SLSQP','dogleg','trust-ncg']:
            try:
                res = scipy.optimize.minimize(op_func, c, args=(f, x, y, j), method=method, jac=op_func_jac)
                if res.success:
                    print("{:16}{:16}".format(method, res.fun))
            except Exception as e:
                print(e)
    
    #return scipy.optimize.minimize(op_func, c, args=(f, x, y, j), method='L-BFGS-B')
    return scipy.optimize.minimize(op_func, c, args=(f, x, y, j), method='L-BFGS-B', jac=op_func_jac)


