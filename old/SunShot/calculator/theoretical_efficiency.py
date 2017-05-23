import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import subprocess
import os
import sys
import pylab as pl
import numpy as np

s = 5.67e-8
C = 293.15
#A = 1
#R = (A * s * ep * C**4) / q


def root(C, K):
    #print('root K',K)
    r = np.roots([-4.0 * K / C**4, 3.0 * K / C**3, 0.0, 0.0, 0.0, (1 + K) * C])
    r = np.real(r[np.imag(r)==0])
    r = r[0]
    return r

vroot = np.vectorize(root)

def get_K(qpp):
    return np.divide(s * C**4, qpp)

e_carnot = lambda H: 1 - C/H

e_rec = lambda H, K, ep: ep * ( 1.0 - K * ( (H/C)**4 - 1 ) )

e = lambda H, K, ep: e_carnot(H) * e_rec(H,K,ep)


pl.rc('text', usetex=True)
pl.rc('font', family='monospace')
pl.rc('font', family='sans-serif')

fileroot = "/home/chuck/Documents/SunShot/Media/image/background/theory/efficiency/"

def line_temp_vs_eta():

    fontPath = "/usr/share/fonts/abc.ttf"
    font = fm.FontProperties(fname=fontPath, size=16)

    H = np.arange(C, 2500)

    ep = 1.0
    K = 4e-4

    print "qpp =", s * C**4 / K

    x = H
    #x = np.log10(H)
    #x = np.divide(1.0,H)
    #x = np.power(H/C, 0.25)

    y2 = e(H, K, ep)
    print x[np.argmax(y2)]

    pl.plot(x, e_carnot(H), 'k-')
    pl.plot(x, e_rec(H, K, ep), 'k--')
    pl.plot(x, y2, 'k-.')
    
    pl.ylim([0,1])
    
    leg = pl.legend(['carnot','rec','overall'], loc=0, prop=font)
   
    pl.xlabel(r"$T_H$ (K)")
    pl.ylabel(r"$\eta$")
    
    # ticks 

    xticks = pl.gca().xaxis.get_majorticklocs()

    H_1 = x[np.argmax(y2)]
    H_2 = C * (1/K + 1)**0.25
    
    loc_n_fmt = [
            (0.,"{0:.0f}"),
            (C,"$T_C$"),
            (500.,"{0:.0f}"),
            (H_1,"$T_{{H1}}$"),
            (1500.,"{0:.0f}"),
            (H_2,"$T_{{H2}}$"),
            (2500.,"{0:.0f}")
            ]
   
    locs = list(a for a,b in loc_n_fmt)

    lbls = [x[1].format(x[0]) for i,x in enumerate(loc_n_fmt)]

    print locs
    print lbls
    
    
    pl.gca().xaxis.set_ticks(locs)
   
    
    pl.xticks(locs, lbls)
  
    
    ax = pl.gca()

    ax.xaxis.get_label().set_fontproperties(font)
    ax.yaxis.get_label().set_fontproperties(font)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(font)

    # show
    save("temp_vs_eta_K_{:.0e}.png".format(K))
    pl.show()


def save(filename):
    pl.savefig(filename)
    subprocess.call(["cp", filename, os.path.join(fileroot, filename)])

def cont():

    f1 = pl.figure()
        
    a1 = f1.add_subplot(111)
   
    qpp = np.logspace(5, 8, 100)
    ep = np.linspace(0.5, 1.0, 100)
    
    print(np.shape(qpp))
    print(np.shape(ep))

    QPP, EP = np.meshgrid(qpp, ep)
    
    K = get_K(QPP)
    
    print(np.shape(K))
    #print('K',K)
    
    
    H = vroot(C, K)
    
    eta = e(H, K, EP)
    
    cs1 = a1.contour(np.log10(K), EP, eta, 10, colors='k')
    
    #qpp_str = r"$log(q''_{\textrm{inc}})$ (W/m$^2$)"

    pl.xlabel(r"log(K)")
    pl.ylabel(r"$\epsilon$")
    
    pl.clabel(cs1)
 
    save("cont.png")

    pl.show()

def line_logK_vs_temp():
    
    qpp = np.logspace(5, 8, 100)
        
    K = get_K(qpp)
    
    H = vroot(C, K)
    
    pl.plot(np.log10(K), H, 'k')
   
    pl.xlabel(r"log(K)")
    pl.ylabel(r'$T_H$ (K)')

    save("logK_vs_temp.png")

    pl.show()



line_temp_vs_eta()
#nondim_line_temp_vs_eta()
#cont()
#line_logK_vs_temp()



