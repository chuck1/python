
from multiprocessing import Process, Pipe

import time

#def wrap_foo_f(foo, p, conns):
#	foo.f(p, conns)

class Foo:
	def f2(self):
		for it in range(3):
			time.sleep(1)

	def f(self, p, conns):
		for it in range(3):
	
			#time.sleep(1)
		
			for c in conns:
				c.send(p)
				r = c.recv()
				print p, " receiving ",r
				
	

foo1 = Foo()
foo2 = Foo()
foo3 = Foo()


c12,c21 = Pipe()
c23,c32 = Pipe()
c13,c31 = Pipe()


p1 = Process(target=Foo.f, args=(foo1, 1, (c12,c13)))
p2 = Process(target=Foo.f, args=(foo2, 2, (c21,c23)))
p3 = Process(target=Foo.f, args=(foo3, 3, (c31,c32)))

p = [p1, p2, p3]

for P in p:
	P.start()

for P in p:
	P.join()


#for P in p:
#	f2()


