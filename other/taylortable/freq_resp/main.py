import numpy as np
import pylab as pl

f1 = lambda h,k: (1.0 - np.exp(1j * k * h * -1.0)) * np.power(1j * k * h, -1.0)

#f2 = lambda h,k: 2.0 * (1.0 - np.exp(-1j * k * h)) / (1j * k * h) / (0.8 + 1.2*np.exp(-1j*k*h))

#f2 = lambda h,k: 2.0 / (1j*k*h) * (0.5 * np.exp(-1j*2.0*k*h) - np.exp(-1j*k*h) + 0.5) / (1.0 - np.exp(-1j*k*h))

#f3 = lambda h,k: (0.5 * np.exp(-1j*3.0*k*h) - np.exp(-1j*2.0*k*h) - 0.5*np.exp(-1j*k*h) + 1) / (1j * k * h)

H = [0.01]
F = [f1]

fig_r = pl.figure()
ax_r = fig_r.add_subplot(111)
ax_r.set_ylabel('real')

fig_i = pl.figure()
ax_i = fig_i.add_subplot(111)
ax_i.set_ylabel('imag')

for h,f in zip(H,F):
	
	
	k = np.linspace(0,100,100)

	y = f(h,k)

	ax_r.plot(k,np.real(y))
	
	ax_i.plot(k,np.imag(y))

leg = ['f1','f2','f3']
leg = ['f1']
ax_r.legend(leg)
ax_i.legend(leg)

pl.show()

