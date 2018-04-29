import numpy as np
import pylinreg

def generate_error(loc, scale, n):
    e = np.random.normal(loc=loc, scale=scale, size=n)
    e = np.reshape(e, (n,1))
    return e

def sample_y(X0, B):
    X = np.append(np.ones(np.shape(X0)), X0, 1)
    # create Y data using true curve and randomly generated distances
    Y = np.dot(X,B)
    return Y

def sample_data(n = 10):

    B = np.array([[10.0],[2.0]])

    X = np.linspace(0.0, 10.0, n)
    X = np.reshape(X, (n,1))
 
    e = generate_error(0.0, 1.5, n)
   
    Y = sample_y(X, B) + e
    
    return X, Y

def _test_1(n):
    
    l1 = _test_weighted(n)
    
    Y1, i0 = l1.response(l1.x)
    
    #print("measurement error")
    #print(e2.flatten())
    print("confidence interval on predictions using curve-fit")
    print(i0.flatten())

    if False:
        plt.figure()
        
        # data
        plt.plot(l1.X0,l1.Y,'o')

        # error bars
        for x,y,e in zip(l1.X0, l1.Y, e2):
            plt.plot([x,x],[y-e,y+e],"b-")

        # plot curve fit
        plt.plot(l1.X0,Y1)

def _test_0(n):
    
    l1 = _test_weighted(n)
    l2 = _test_unweighted(n)
    
    Y1, i1 = l1.response(l1.x)
    Y2, i2 = l2.response(l2.x)
    
    #print("measurement error")
    #print(e2.flatten())
    print("confidence interval with weighting")
    print(i1.flatten())
    print("confidence interval without weighting")
    print(i2.flatten())

    if False:
        fig,ax = plt.subplots()
        
        # data
        plt.plot(l1.X0,l1.Y,'o')

        # error bars
        for x,y,e in zip(l1.X0, l1.Y, e2):
            plt.plot([x,x],[y-e,y+e],"b-")

        # plot curve fit
        plt.plot(l1.X0,Y1,label="weighted")
        plt.plot(l2.X0,Y2,label="unweighted")

        ax.legend()

def _test_weighted(n):

    X, Y = sample_data(n)

    l = pylinreg.LinearRegression()
 
    e = generate_error(4.0, 1.5, n)
  
    l.W = np.diagflat(1.0 / e)
    l.x = X
    l.y = Y
    
    l.calc()

    return l

def _test_unweighted(n):

    X, Y = sample_data(n)

    l = pylinreg.LinearRegression()
 
    l.x = X
    l.y = Y
    
    l.calc()

    return l

def test_unweighted():
    _test_unweighted(10)

def test_weighted():
    _test_weighted(10)

def test_0():
    n = 10
    _test_0(n)

def test_1():
    n = 10
    _test_1(n)



