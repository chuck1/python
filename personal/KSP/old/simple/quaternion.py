
import math
import numpy as np



class quaternion:
	def __init__(self, q):
		self.q = np.array(q)

	def add(self, q):
		return quaternion(self.q + q)

	def addeq(self, q):
		self.q += q

	def dot(self, q):
		return np.dot(self.q, q)
	
	def magnitude(self):
		return np.linalg.norm(self.q)

 	def magnitudeSquared(self):
		return self.magnitude()**2

	def negate(self):
		pass

	def scale(self):
		pass

	def conjugate(self):
		return quaternion([-self.q[0], -self.q[1], -self.q[2], self.q[3]])

	def normalize(self):
		s = self.magnitude()
		return quaternion(self.q / s)

	def concat(self, q):
		q0 = self.q
		q1 = q.q

		x0 = q0[0]
		y0 = q0[1]
		z0 = q0[2]
		w0 = q0[3]
		x1 = q1[0]
		y1 = q1[1]
		z1 = q1[2]
		w1 = q1[3]
		
		result = np.zeros((4,))

		print 'result',result

		result[0] = w0 * x1 + x0 * w1 + y0 * z1 - z0 * y1;
		result[1] = w0 * y1 - x0 * z1 + y0 * w1 + z0 * x1;
		result[2] = w0 * z1 + x0 * y1 - y0 * x1 + z0 * w1;
		result[3] = w0 * w1 - x0 * x1 - y0 * y1 - z0 * z1;

		print 'result',result

		return quaternion(result);

	def toVector(self):
		q = self.q
		return np.array([q[0], q[1], q[2]])

	def rotate(self, vec):
		p = quaternion([vec[0], vec[1], vec[2], 0])
		
		return self.concat(p).concat(self.conjugate()).toVector();

def fromAngleAxis(angle, axis):
	#print angle,axis
	halfAngle = 0.5 * angle
	#print halfAngle
	sin = math.sin(halfAngle);
	
	axis /= np.linalg.norm(axis);
	print axis

	q = quaternion([sin * axis[0], sin * axis[1], sin * axis[2], math.cos(halfAngle)])
	q = q.normalize()

	return q

def fromToRotation(_from, to):
	
	#_from = numeric.divVS(_from, numeric.norm2(_from))
	_from = np.linalg.norm(_from)

	#to = numeric.divVS(to, numeric.norm2(to))
	to = np.linalg.norm(to)

	dot = np.dot(_from, to)
	
	if dot > (1.0 - 1e-6):
		return quaternion([0, 0, 0, 1])
	
	elif (dot < -(1.0 - 1e-6)):
		return fromAngleAxis(math.pi, [0, 0, 1])
	else:
		q = np.zeros((4,1))
		
		s = math.sqrt(2 * (1 + dot))

		invs = 1 / s
		
		q[0] = (_from[1] * to[2] - _from[2] * to[1]) * invs
		q[1] = (_from[2] * to[0] - _from[0] * to[2]) * invs
		q[2] = (_from[0] * to[1] - _from[1] * to[0]) * invs
		q[3] = 0.5 * s
		
		return quaternion(np.linalg.norm(q))

def fromVector(vec):
	return quaternion([vec[0], vec[1], vec[2], 0])







