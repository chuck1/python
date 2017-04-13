
import scipy.optimize
import numpy

def op_func(c, f, x, y):
    y1 = f(x,c)
    e = numpy.sum(numpy.power(y1 - y,2))
    return e

 
"""
the function shall be of the form
y = f(x[0], x[1]...)

the x data shall be an array with m rows and n columns
where m is the number of inputs to the function
and n is the number of data points

the y data shall be an array with 1 row and n columns

"""
def fit(f, x, y, c):

    y1 = f(x,c)

    e = numpy.sum(numpy.power(y1 - y,2))

   
    for method in ['Nelder-Mead','Powell','CG','BFGS','Newton-CG','L-BFGS-B','TNC','COBLYA','SLSQP','dogleg','trust-ncg']:
        try:
            res = scipy.optimize.minimize(op_func, c, args=(f, x, y), method=method)
            if res.success:
                print(method, res.fun)
        except: pass

    res = scipy.optimize.minimize(op_func, c, args=(f, x, y), method='L-BFGS-B')
    
    return res


