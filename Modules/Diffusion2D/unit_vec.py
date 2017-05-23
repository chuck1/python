

def sign(x):
	return -1 if x < 0 else 1

def is2v(i,s):
	return (i + 1) * s
def v2is(v):
	return abs(v) - 1, sign(v)
	
def fwd(A, n):
	a,s = v2is(A)

	b = (a + n) % 3
	
	B = is2v(b,s)
	return B

def fwd_dist(A, B):
	a,sa = v2is(A)
	b,sb = v2is(B)
	
	d = b - a
	d = d if d > 0 else d + 3
	return d

def bwd(A, n):
	B = fwd(A, 2 * n)
	return B

def bwd_dist(A, B):
	d = fwd_dist(B, A)

def nxt(A, n = 1):
	if A > 0:
		return fwd(A, n)
	else:
		return bwd(A, n)

def nxt_dist(A, B):
	if A > 0:
		return fwd_dist(A, B)
	else:
		return bwd_dist(A, B)
	
def cross(A,B):
	#print A,B
	
	a,sa = v2is(A)
	b,sb = v2is(B)
	
	if b == (a+1) % 3:
		c = ((a+2) % 3) + 1
	else:
		c = ((a+1) % 3) + 1
		c = -c
	
	c *= sa * sb
	
	#print a, b, c

	return c


class LocalCoor:
	# store as [[-1, 1],[-2, 2],[-3, 3]]
	
	def __init__(self, Z):
		self.Z = Z
		self.X = nxt(self.Z)
		self.Y = nxt(self.X)
		
		self.x, self.xs = v2is(self.X)
		self.y, self.ys = v2is(self.Y)
		self.z, self.zs = v2is(self.Z)
			
	def glo_to_loc(self, G):
		sg = sign(G)
		sz = sign(self.Z)
		
		d = nxt_dist(abs(self.Z), abs(G))
		
		L = sg * nxt(3 * sz, d)
		
		return L
		
	def loc_to_glo(self, L):
		G = sign(L) * nxt(self.Z, abs(L) % 3)
		return G

