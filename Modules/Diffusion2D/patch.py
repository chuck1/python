from face import *
from util import *

class Patch(LocalCoor):
	def __init__(self, group, name, normal, indices, x, nx, v_bou):
		
		LocalCoor.__init__(self, normal)
		
		self.group = group
		self.name = name

				
		
		#if not np.shape(self.v_bou) == (2,2):
		#	print self.v_bou
		#	raise ValueError('')
		
		#print 'T_0',T_0

		self.indices = indices
		
		NX = len(indices[self.x])-1
		NY = len(indices[self.y])-1

		# expand scalar v_bou values
		for k in v_bou.keys():
			if isinstance(v_bou[k][0][0], float): v_bou[k][0][0] = np.ones(NY)*v_bou[k][0][0]
			if isinstance(v_bou[k][0][1], float): v_bou[k][0][1] = np.ones(NY)*v_bou[k][0][1]
			if isinstance(v_bou[k][1][0], float): v_bou[k][1][0] = np.ones(NX)*v_bou[k][1][0]
			if isinstance(v_bou[k][1][1], float): v_bou[k][1][1] = np.ones(NX)*v_bou[k][1][1]

		
		# make sure indices are sorted properly
		rev = True if normal < 0 else False
		indices[self.x] = sorted(indices[self.x], reverse=rev)
		indices[self.y] = sorted(indices[self.y], reverse=rev)
		
		# alloc faces array
		faces = np.empty((NX,NY), dtype=object)
		
		for i in range(NX):
			for j in range(NY):
				I = indices[self.x][i]
				J = indices[self.y][j]
				M = indices[self.x][i+1]
				N = indices[self.y][j+1]
				
				Is = min(I,M)
				Js = min(J,N)
				Ms = max(I,M)
				Ns = max(J,N)
				
				ext = [[x[self.x][Is], x[self.x][Ms]], [x[self.y][Js], x[self.y][Ns]]]
				
				numx = nx[self.x][min(I,M)]
				numy = nx[self.y][min(J,N)]
				
				#print "I,J",I,J
				
				pos_z = x[self.z][indices[self.z]]
				
				
				faces[i,j] = Face(self, normal, ext, pos_z, [numx, numy])
			
				# unique to current setup
				# create temperature and source spreader equations
				
				
				faces[i,j].create_equ('T', self.group.prob.equs['T'])
				
				faces[i,j].create_equ('s', self.group.prob.equs['s'])
				faces[i,j].equs['s'].flag['only_parallel_faces'] = True
				
				# alloc v_bou dict in face
				faces[i,j].v_bou = {}
				
				for k in v_bou.keys():
					# alloc face v_bou list
					faces[i,j].v_bou[k] = [[0,0],[0,0]]
					
					# set face v_bou
					#logging.debug("".format(np.shape(v_bou[k][)))

					if i == 0:	faces[i,j].v_bou[k][0][0] = v_bou[k][0][0][j]
					if i == NX-1:	faces[i,j].v_bou[k][0][1] = v_bou[k][0][1][j]
					if j == 0:	faces[i,j].v_bou[k][1][0] = v_bou[k][1][0][i]
					if j == NY-1:	faces[i,j].v_bou[k][1][1] = v_bou[k][1][1][i]

				
				
		self.npatch = np.array([NX,NY])

		self.faces = faces;

		self.grid_nbrs()

	def create_equ(self, name, v0, v_bou, k, al):
		for f in self.faces.flatten():
			f.create_equ(name, v0, v_bou, k, al)
	
	
	def set_v_bou(self, equ_name, v_bou):
		for f in self.faces.flatten():
			f.equs[equ_name].v_bou = np.array(v_bou)
	
	

	# value statistics
	def max(self, equ_name):
		v = float("-inf")

		for f in self.faces.flatten():
			a = f.equs[equ_name].max()
			v = max(v,a)
			print "a v",a,v
		
		return v

	def grid_nbrs(self):
		nx,ny = np.shape(self.faces)
	
		for i in range(nx):
			for j in range(ny):
				f1 = self.faces[i,j]
				if i > 0:
					if not f1.conns[0,0]:
						connect(f1, 0, 0, self.faces[i-1,j], 0, 1)
				if i < (nx-1):
					if not f1.conns[0,1]:
						connect(f1, 0, 1, self.faces[i+1,j], 0, 0)
				if j > 0:
					if not f1.conns[1,0]:
						connect(f1, 1, 0, self.faces[i,j-1], 1, 1)
				if j < (ny-1):
					if not f1.conns[1,1]:
						connect(f1, 1, 1, self.faces[i,j+1], 1, 0)

	def plot(self, equ_name, fig, V, Vg):
		ax1 = fig.ax1
		ax2 = fig.ax2
		
		for f in self.faces.flatten():
			con1, con2 = f.plot(equ_name, ax1, ax2, V, Vg)
		
		fig.text.set_text(fig.text.get_text() + ' ' + self.name)
		
		return con1, con2




