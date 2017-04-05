#!/usr/bin/env python

import numpy as np
import math
import scipy.optimize

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p',action='store_true')
args = parser.parse_args()

if args.p:
    import pylab as pl

PT = np.array([
        1.5,
        1.5,
        2.0,
        2.0
        ])

RE = np.array([
        18.9,
        18.9,
        12.6,
        12.6
        ])

D = np.array([
        1.88e-4,
        2.50e-4,
        1.88e-4,
        2.50e-4
        ])

f = np.array([
        17.8,
        9.3,
        46.5,
        27.7
        ])


if args.p:
    fig = pl.figure()

    # plot 1
    ax = fig.add_subplot(121)
    
    ind1 = D == D[0]
    ind2 = D == D[1]
    ax.plot(PT[ind1],f[ind1],'o', label="D = {0} m".format(D[0]))
    ax.plot(PT[ind2],f[ind2],'s', label="D = {0} m".format(D[1]))

    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.)

    

    ax.set_xlabel('PT')
    ax.set_ylabel('f')
  
    ax.set_xlim([1.4,2.1])

    # plot 2
    ax = fig.add_subplot(122)
    
    ind1 = PT == PT[0]
    ind2 = PT == PT[2]
    ax.plot(D[ind1],f[ind1],'o', label="PT = {0}".format(PT[0]))
    ax.plot(D[ind2],f[ind2],'s', label="PT = {0}".format(PT[2]))
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.)
    
    ax.set_xlabel('D (m)')
    ax.set_ylabel('f')

    ax.xaxis.get_major_formatter().set_powerlimits((0, 1))

    ax.autoscale_view(tight=False, scalex=False, scaley=True)

    pl.subplots_adjust(top=0.8)

    pl.show()



# x1 = PT
# x2 = D
# y = f
def fitfun(p, x1, x2):
    return p[0] * x1**p[1] * x2**p[2]
    
def errfun(p, x1, x2, z_meas):
    return (fitfun(p, x1, x2) - z_meas)




#xl = np.linspace(np.min(xd),np.max(xd),100)
#fl = math.exp(X[0]) * xl

p0 = [1e-8, 3.0, -2.0]

p,_ = scipy.optimize.leastsq(errfun, p0, args=(PT, D, f))



if args.p:

    xd = PT**p[1] * D**p[2]
    
    xl = np.linspace(np.min(xd),np.max(xd),100)  
    fl = p[0] * xl  
    
    fig = pl.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(xd,f,'o')

    ax.plot(xl,fl,'-')

    ax.set_xlabel('PT^b D^c')
    ax.set_ylabel('f')

    pl.show()

err1 = errfun(p, PT, D, f)

print "f   =",f
#print "p0  =",p0
print "p   =",p
print "err =",err1
print "%err=",err1 / f * 100.0

np.save('p',p[0])


