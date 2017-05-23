
import pickle
import inspect
import numpy as np
import logging

#import oodb.classes
#import oodb.class_util
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
        for name in oodb.util.get_data_filenames(oodb.ROOT):
            logging.info(name)
            with open(name, 'rb') as f:
                # a list of objects
                lst = pickle.load(f)
                self.lst += lst
                
            #logging.info(lst)

        #for o in self.lst:
        #    print(o.id)

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
            return None,None

            logging.info(i)
            raise Exception()

        return o,ind
    
    def objects(self, filters={}, objtype=None, tests=[]):

        
        def test1(o):
            for k,v in filters.items():
                if o.get(k) != v:
                    return False
            return True
        
        def test2(o):
            if not objtype:
                return True

            if isinstance(o, objtype):
                return True
            else:
                return False

        def test3(o):
            for t in tests:
                if not t(o):
                    return False
            return True

        for o in self.lst:
            if test1(o):
                if test2(o):
                    if test3(o):
                        yield o

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
            logging.info(fmtstr.format(*r))
            

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

        #logging.info(str)
        #logging.info(attr_names)
        #logging.info(str.format(*attr_names))

        rows = list(list(get_value(s, an) for an in attr_names) for s in gen)

        return View(headers, rows)


    def save(self):
        logging.info('save')
        # rewrite database
        oodb.util.rm_data_files(oodb.ROOT)
        oodb.util.save_to_next(oodb.ROOT, self.lst)
    
    ## replace
    # @param obj new object
    # @param r id
    def replace(self, obj, r):

        obj.id = r
        
        _,ind = self.get_object_index(r)
        
        self.lst[ind] = obj
        

        # rewrite database
        self.save()
