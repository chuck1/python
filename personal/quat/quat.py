import math
import numpy as np

class quat:
	def __init__(self,x,y,z,t):
		
		self.x = x * math.sin(t/2)
		self.y = y * math.sin(t/2)
		self.z = z * math.sin(t/2)
		
		
		
		self.w = math.cos(t/2)
		
	def __mul__(self,q):
		r = quat()
		
		r.w = self.w * 
		
		
def slerp(q0,q1,u):
	q = math.sin((1-u) * t) / math.sin(t) * q0 + math.sin(u*t) / math.sin(t) * q1
	return q
	




q0 = quat(1,0,0,0)





