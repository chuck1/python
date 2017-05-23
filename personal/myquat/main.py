from sympy import *
#import numpy as np


def matsim(A):
	for a in range(np.size(A,0)):
		for b in range(np.size(A,1)):
			A[a,b] = expand(A[a,b])


	return A

def test(a,b):
	a = matsim(a)
	b = matsim(b)

	#print a
	#print b
	
	e = a==b

	if np.all(e):
		print True

		print a
		print b

	else:
		print a
		print b

		print e

		
def A(q):
	#q = np.array(np.reshape(q,(4)))
	return Matrix([
		[ q[0],  q[1],  q[2],  q[3]],
		[-q[1],  q[0], -q[3],  q[2]],
		[-q[2],  q[3],  q[0], -q[1]],
		[-q[3], -q[2],  q[1],  q[0]]])

def B(q):
	#q = np.reshape(q,(4))
	return Matrix([
		[ q[0], -q[1], -q[2], -q[3]],
		[ q[1],  q[0], -q[3],  q[2]],
		[ q[2],  q[3],  q[0], -q[1]],
		[ q[3], -q[2],  q[1],  q[0]]])

def quat(q):
	q = Matrix(4,1,[q[0], q[1], q[2], q[3]])
	#q = np.reshape(q, (4,1))
	return q

def conj(q):
	q = Matrix([[q[0], -q[1], -q[2], -q[3]]])
	#q = np.reshape(q, (4,1))
	return q

def mul(X):
	Y = X[0]
	for a in range(1,len(X)):
		Y = np.dot(Y, X[a])
	
	return Y

def quatmul(a,b):
	
	va = Matrix(a[1:])
	vb = Matrix(b[1:])
	
	#print np.shape(va)
	#print np.shape(vb)
	
	#print a[0]*b[0]
	#print np.dot(va,vb)
	
	#print type(a[0]*b[0])
	
	c = Matrix(4,1,a)
	
	c[0] = a[0]*b[0] - va.dot(vb)
	
	vc = a[0]*vb + b[0]*va + va.cross(vb)


	c[1] = vc[0]
	c[2] = vc[1]
	c[3] = vc[2]
	
	return c


asym = quat(symbols('a0:4'))
bsym = quat(symbols('b0:4'))
csym = quat(symbols('c0:4'))

u = quat([1,0,0,0])

a = quat(asym)
b = quat(bsym)

#test(mul((B(a), b)), mul((A(conj(b)), a)))
#test(mul((A(a), b)), mul((B(b), conj(a))))
#test(mul((A(a), b)), mul((B(b), conj(a))))


#test(mul((B(a),u)), a)
#test(mul((A(a),u)), conj(a))

# be careful, this is misleading...
# A(a*) a = B(a) a
# does not mean
# A(a*) = B(a)
#test(mul((A(conj(a)), a)),mul((B(a), a)))

"""
test(
		B(
			mul((A(a),b))
			),
		mul((
			A(a),B(b)
			))
		)
"""


"""
test(
		quatmul(a,b),
		np.transpose(mul((np.transpose(b),B(conj(a)))))
		)
"""

"""
test(
		A(mul((A(a),b))),
		A(mul((B(b),conj(a)))))


test(
		mul((
			A(mul((A(a),b))),
			c)),
		mul((
			B(c),
			conj(mul((A(a),b))))))


test(
		conj(mul((A(a),b))),
		mul((A(b),a)))

test(
		mul((
			A(mul((A(a),b))),
			c)),
		mul((
			B(c),
			mul((A(b),a)))))
"""

"""
test(
		mul((
			A(mul((A(a),b))),
			c)),
		mul((
			B(c),
			A(b),
			a)))


test(
		conj(
			mul((A(a),b))
			),
		mul((
			A(b),
			a))
		)




d = matsim(
		mul((
			A(a),
			B(a)
			))
		)
print d[1:,1:]
"""
"""
test(
		quatmul(quatmul(a,b),conj(a)),
		mul((A(a),B(a),b))
		)
"""

#test(quatmul(a,b), mul((B(a),b)))

"""
test(
		mul((
			A(a),
			B(b)
			)),
		mul((
			B(b),
			A(a)
			))
		)
"""
"""
test(
		B(
			mul((
				B(a),
				b
				))
			),
		mul((
			B(a),
			B(b)
			))
		)
"""

"""
test(
		np.transpose(mul((
			B(a),
			B(b)
			))),
		mul((
			B(conj(b)),
			B(conj(a))
			))
		)
"""

def rotations():
	o1,o2,o3 = symbols('o1:4')

	o = quat([0, o1, o2, o3])

	t3, t3p = symbols('t, tp')

	t = quat([0, 0, 0, t3])
	tp = quat([0, 0, 0, t3p])
	
	c = quatmul(conj(o),t) + tp + quatmul(t,o)
	
	pprint(c)
	
	
	

	
rotations()

#print mul((B(t), o))
#print mul((B(conj(o)), t))
#print mul((B(t), o)) + mul((B(conj(o)), t)) + tp


"""
c = A(a)

d = c.det()
d = expand(d)

e = (a.dot(a))**2
e = expand(e)

pprint(d)
pprint(e)

print d==e
"""

#e = c**(-1)
#e = expand(e)

#e = simplify(e)

#pprint(e)

"""
c = B(conj(a))*B(a)
pprint(c)
c = B(a)*B(conj(a))
pprint(c)

c = quatmul(a,b)
d = quatmul(b,a)

pprint(c)
pprint(d)
"""


#pprint(quatmul(a,b))
#pprint(quatmul(conj(b),a))

