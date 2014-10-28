
import pickle
import inspect
import numpy as np

import oodb.classes
import oodb.class_util
import oodb.util
import oodb.gui

# get an oodb Value object from an oodb Object
def get_value(o, attr_desc):
	
	if isinstance(attr_desc, str):
		try:
			a = getattr(o, attr_desc)
		except:
			# attribute doesnt exist
			return oodb.make_value(o, attr_desc, 'None')
		else:
			# attribute exists
			if not a:
				return oodb.make_value(o, attr_desc, 'None')
			else:
				return oodb.make_value(o, attr_desc, a)

	else:
		# external function
		l = lambda: attr_desc[1](o)
		return oodb.Method(l)

class View:
	def __init__(self, headers, rows):
		self.r = len(rows)
		self.c = len(headers)
		
		self.headers = headers
		self.rows = rows

class Database:
	def __init__(self):
        
		self.lst = []
		for name in oodb.util.get_data_filenames():
			   
			with open(name, 'rb') as f:
				# a list of objects
				lst = pickle.load(f)

				self.lst += lst
				
			#print(lst)

		for o in self.lst:
			o.resolve(self)

	def __del__(self):
		#self.save()
		pass

	def get_object_index(self, i):
		found = False
		for ind in range(len(self.lst)):
			if self.lst[ind].id == i:
				found = True
				o = self.lst[ind]
				break

		if not found:
			print(i)
			raise Exception()

		return o,ind

	def get_object(self, i):
		o,_ = self.get_object_index(i)
		return o



	def change_type(self, i, A):

		o,ind = self.get_object_index(i)
		
		a = A(i)

		a.__dict__ = o.__dict__
		
		self.lst[ind] = a
    
	def display(self, gen, attr_names):

		rows = self.gen_rows()

		# auto col width
		m = [0]*N
		for r in rows:
			for c in range(len(r)):
				m[c] = max(m[c], len(r[c])+1)


		fmtstr = ('{{:{}}}'*N).format(*m)


		for r in rows:
			print(fmtstr.format(*r))
			

		return rows

	def gen_rows(self, gen, attr_names):
        
		headers = []
		for an in attr_names:
			if isinstance(an, str):
				headers.append(an)
			else:
				headers.append(an[0])

		rows = []

		N = len(attr_names)

		fmtstr = '{:32}'*N

		#print(str)
		#print(attr_names)
		#print(str.format(*attr_names))

		rows = list(list(get_value(s, an) for an in attr_names) for s in gen(self.lst))

		return View(headers, rows)


	def save(self):
		print('save')
		# rewrite database
		oodb.util.rm_data_files()
		oodb.util.save_to_next(self.lst)
		
	def replace(obj, r):

		obj.id = r
		
		_,ind = self.get_object_index(r)
		
		self.lst[ind] = obj
		

		# rewrite database
		self.save()
