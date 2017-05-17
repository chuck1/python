import sys
import os
import re
import shutil
import numpy as np
import xml.etree.ElementTree as ET
import logging

import Sci.Fluids
import Sci.Data.Flux_Map
import Fluent as FLU

# global constants

dir_home = os.environ['HOME']
dir_mohr = "/nfs/mohr/sva/work/rymalc/bin"

dir_scheme = os.path.join(dir_home, "Documents", "Programming", "Scheme")

class clr:
	END	= '\033[0m'
	RED	= '\033[31m'
	GREEN	= '\033[32m'
	YELLOW	= '\033[33m'
	BLUE	= '\033[34m'
	MAGENTA	= '\033[35m'
	
	
	
	
	

var_def = {
		'GEO_SOLAR_WIDTH':'SOLAR_WIDTH',
		'GEO_SOLAR_LENGTH':'SOLAR_LENGTH'
		}

def prnt(a):
	logging.info(a)

def print_tree(root,tab = 0):
	text = root.text
	if root.text:
		text = re.sub('[\t\n]','',root.text)
	else:
		text = ''
	logging.info("\t" * tab, root.tag, root.attrib, text)
	for child in root:
		#logging.info("\t" * tab, child.tag, child.attrib, re.sub('[\t\n]','',child.text))
		print_tree(child, tab + 1)

def text_to_dir(text):
	number = int(text)
	dir = "x{0:04d}".format(number)
	return dir
def index_to_dir(text):
	dir = "x{0:04d}".format(index)
	return dir


def strip_white(text):
	#logging.info("before: <<<{0}>>>".format(text))
	text = re.sub('^[\t\n ]*','',text)
	text = re.sub('[\t\n ]*$','',text)
	#logging.info("after:  <<<{0}>>>".format(text)
	return text
def process_array(text):
	lines = re.split('\n',text)
	lines = [strip_white(line) for line in lines]
	lines = [line for line in lines if line]

	test = lines[0]
	test = re.split(',',test)
	
	rows = len(lines)
	cols = len(test)
	
	ret = np.zeros((rows,cols))
	
	for line,i in zip(lines,range(rows)):
		#logging.info(line
		for e,j in zip(re.split(',', line), range(cols)):
			ret[i,j] = float(e)
	return ret





class Data:
	pass

class Config:


	def __init__(self, path, master):

		self.data = Data()
		self.var = {}
		self.sources = []
		self.config = []
		
		if master:
			self.master = master
		else:
			self.master = self

	
		path = os.path.abspath(path)

		logging.info(clr.BLUE + "Config File \"{0}\"".format(path) + clr.END)

		self.path = path
		
		h,_ = os.path.split(path)
		h,x = os.path.split(h)
		#_,t = os.path.split(h)
	
		self.x = int(x[1:])
	
		#logging.info(h, dir_mohr

		self.cat = os.path.relpath(h, dir_mohr)
		
		#logging.info(self.cat, self.x
	
	def run(self):
		self.get_root(self.path)

	def get_root(self, path):
		#logging.info("loading '{0}'".format(filename)

		if not os.path.isfile(path):
			raise ValueError(clr.RED + "{0}: No such file.".format(path) + clr.END)

		self.tree = ET.parse(path)
		self.root = self.tree.getroot()
		
		self.load_var_from_root(self.root)

		self.include_files(self.root, path)

	def include_files(self, root, path):
		# path - path of xml file which is source of root

		#logging.info("include files for \"{0}\"".format(path)
		
		dir1, filename1 = os.path.split(path)
		
		for child in root.findall('include'):
			#logging.info("\t", child.tag, child.attrib
			
			type = child.attrib['type']
			dir2 = child.attrib['dir']
			
			dir3 = self.include_dir(dir1,dir2)

			if type == 'config':
				index = int(child.attrib['index'])
				
				x = "x{0:04d}".format(index)
				
				src = os.path.join(dir3, x, 'config.xml')
				
				conf = Config(src, self.master)
				conf.run()

				self.config.append(conf)

			elif type == 'copy':
				filename2 = child.attrib['name']
				
				src = os.path.join(dir3, filename2)

				dest = os.path.join(self.master.var["DIR_BINARY"], filename2)
				
				shutil.copyfile(src, dest)

				self.sources.append(src)	
			elif type == 'script':
				try:
					filename2 = child.attrib['name']
				except:
					filename2 = 'script.py'
				
				src = os.path.join(dir3, filename2)

				self.run_script(src)
				
				self.sources.append(src)
			else:
				raise ValueError("undefined include type \"{0}\"".format(type))


	def include_dir(self, dir1, dir2):
		if dir2 == "here":
			return dir1
		else:
			return os.path.join(dir_mohr, dir2)

	def load_var_from_root(self, root):
		for child in root.findall('var'):
			self.load_var(child)
		for child in root:
			self.load_var_from_root(child)

	def load_var(self, child):
		#logging.info(child.attrib, child.text
		
		name = child.attrib['name']
		type = child.attrib['type']
		text = child.text

		logging.info("load \"{0}\"".format(name))
		
		text = text.strip()

		if type == 'string':
			val = text
		elif type == 'int':
			val = int(text)
		elif type == 'float':
			val = float(text)
		elif type == 'array':
			val = process_array(text)
		elif type == 'bool':
			if text == 'true':
				val = True
			elif text == 'false':
				val = False
			else:
				raise ValueError(clr.RED + "Bad bool value: \"{0}\"".format(text) + clr.END)
		else:
			raise ValueError(clr.RED + "Bad var type: \"{0}\"".format(type) + clr.END)

		self.master.var[name] = val

	def float_or_var(self, text):
		m = re.search("^@(\w+)@$", text)
		if m:
			text = m.group(1)
			logging.info("looking for {0}".format(text))
			val = self.var[text]
		else:
			val = float(text)
		
		return val


	def run_script(self, path):
		variables = {}

		logging.info(clr.GREEN + "executing scricpt \"{0}\"".format(path) + clr.END)

		execfile(path, variables)

		variables['func'](self.master)





class Case(Config):
	
	def __init__(self, path):
		Config.__init__(self, path, None)

		self.var["DIR_SOURCE"], _ = os.path.split(path)
		self.var["DIR_BINARY"] = os.path.join(self.var["DIR_SOURCE"], 'build')
		
		self.run()
		
		#logging.info(self.sources

	# functions
	
	def set_var(self, name, val):
		self.var[name] = val

	def get_var(self, name):
		try:
			return self.var[name]
		except:
			try:
				def_name = var_def[name]
				self.var[name] = self.var[def_name]
				return self.var[name]
			except:
				logging.error("no variable \"{0}\" found".format(name))
				logging.error("variables are:")
				for k in self.var.keys():
					logging.error('\t' + k)
				raise ValueError("var not found")
	

		

	def configure(self, lines):
		lines_configured = []
		for line in lines:
			#logging.info(line[:-1]
			matches = re.findall("@(\w+)@",line)
			for m in matches:
				if not m in self.var:
					logging.error("no variable \"{0}\" found".format(m))
					logging.error("required in:")
					logging.error(line[:-1])
					logging.error("variables are:")
					for k in self.var.keys():
						logging.error('\t' + k)
					raise 0
				v = self.var[m]
				line = re.sub("@" + m + "@", "{0}".format(v), line)
			lines_configured.append(line)
			#logging.info(line[:-1]
		return lines_configured
	
	
	def get_lines_configured(self, path):
		#logging.info("configuring '{0}'".format(path)
		f = open(path,'r')
		lines = f.readlines()
		lines = self.configure(lines)
		return lines
	
	

	
	def calculate_fluid(self):
		fluid_name = self.var['FLUID_NAME']
		self.fluid = Sci.Fluids.Fluid(fluid_name)
	
	def calculate_inlet_rho(self):
		temp = self.var['INLET_TEMPERATURE']
		
		rho = self.fluid.get('density',temp)
		
		self.var['INLET_RHO'] = rho
		
	def calculate_inlet_mass_flow_rate(self):
		f = self.var['SOLAR_FLUX']
		
		t0 = self.var['INLET_TEMPERATURE']
		t1 = self.var['OUTLET_TEMPERATURE']
		
		dh = self.fluid.enthalpy_change(t0,t1)
		
		w = self.get_var('GEO_SOLAR_WIDTH')
		l = self.get_var('GEO_SOLAR_LENGTH') 
		
		m = f * w * l / dh
		
		self.var['INLET_MASS_FLOW_RATE'] = m


	# =====================================
	# functions to populate fluent journal

	def script_fluent_general(self):
		yield "(define bin_dir \"/nfs/mohr/sva/work/rymalc/bin/\")"
		yield "(define home_dir \"/nfs/stak/students/r/rymalc/\")"
		yield "(define working_dir \"{0}\")".format(self.var["DIR_SOURCE"])
		yield "(define dir_scheme \"{0}\")".format(dir_scheme)
		yield "(load (string-append dir_scheme \"/Unsorted/load_schemes.scm\"))"
		yield "/file/read-case \"case.cas\""

	def script_fluent_models(self):
		if self.var["FLU_ENERGY"]:
			yield "/define/models/energy yes no no no yes"

		s = self.var["FLU_VISCOUS"]
		if s == "kw-standard":
			yield "/define/models/viscous/kw-standard yes"
		elif s == "laminar":
			yield "/define/models/viscous/laminar yes"
		else:
			raise ValueError("bad viscous option")
		

		
	def script_fluent_udf(self):
		lib_name = "libudf"
		file_c = os.path.join(os.environ["HOME"], "Documents/Programming/C/Fluent/udf.c")
			
		yield "/define/user-defined/compiled-functions compile \"{0}\" yes \"{1}\" \"\" \"\"".format(lib_name, file_c)
		yield "/define/user-defined/compiled-functions load \"{0}\"".format(lib_name)
	
	def flu_jou_materials_db_user(self, name):
		yield "/define/materials/data-base/database-type user-defined \"{0}\"".format(name)

	def flu_jou_materials_copy(self, type, name):
		yield "/define/materials/copy {0} {1}".format(type, name)
	
	# boundary conditions
	def flu_jou_mass_flow_inlet(self, name, child):
		str = FLU.mass_flow_inlet(name,
				self.var["FLU_ENERGY"],
				self.var["FLU_VISCOUS"],
				self.get_var("MASS_FLOW_RATE"),
				self.var["INLET_TEMPERATURE"])
		for s in str: yield s
	
	def flu_jou_wall(self, name, child):
		heat_flux_spec	= child.attrib["heat_flux_specification"]
		material	= child.attrib["material"]
		heat_flux	= self.float_or_var(child.attrib["heat_flux"])
		
		if heat_flux_spec == "constant":
			for s in FLU.wall_heat_flux_const(name, heat_flux, material): yield s
		else:
			raise ValueError("bad heat flux spec")
	
	# ---
	def script_fluent_materials(self):
		path = os.path.join(dir_mohr, "material/material.scm")

		for s in self.flu_jou_materials_db_user(path): yield s
		for s in self.flu_jou_materials_copy("fluid", "carbon-dioxide"): yield s
		for s in self.flu_jou_materials_copy("fluid", "ms1"): yield s
		for s in self.flu_jou_materials_copy("solid", "haynes230"): yield s


	def script_fluent_cell_zones(self):
		for child in self.root.findall("cell"):
			name = child.attrib["name"]
			type = child.attrib["type"]
			material = child.attrib["material"]
			strs = FLU.cell_zone(
					name,
					type,
					material,
					self.var["FLU_ENERGY"],
					self.var["FLU_VISCOUS"])
			for s in strs: yield s

	def script_fluent_boundary_conditions(self):
		for child in self.root.findall("boundary"):
			name = child.attrib["name"]
			type = child.attrib["type"]

			if type == "mass_flow_inlet":
				for s in self.flu_jou_mass_flow_inlet(name, child): yield s
			elif type == "wall":
				for s in self.flu_jou_wall(name, child): yield s
			else:
				raise ValueError("bad type {0}".format(repr(type)))

	def script_fluent_solve(self):
		yield "/mesh size-info"
		yield "/solve/initialize/hyb-initialization"
		yield "/solve/it 500"

	def script_fluent_export(self):
		yield "(resolve_surface_id \"inlet\"  \"/report/surface-integrals/area-weighted-avg ~a () pressure no"
		yield "(resolve_surface_id \"outlet\" \"/report/surface-integrals/area-weighted-avg ~a () pressure no"
		yield "(resolve_surface_id \"outlet\" \"/report/surface-integrals/mass-weighted-avg ~a () temperature no"
		yield "(resolve_surface_id \"heated\" \"/report/surface-integrals/area-weighted-avg ~a () temperature no"


	

	def script_fluent(self):
		strs = []

		strs += self.script_fluent_general()
		strs += self.script_fluent_models()
		#strs += self.script_fluent_udf()
		strs += self.script_fluent_materials()
		strs += self.script_fluent_cell_zones()
		strs += self.script_fluent_boundary_conditions()
		strs += self.script_fluent_solve()
		strs += self.script_fluent_export()
		
		#print strs
		str = "\n".join(strs)
		
		return str

	def script_fluent_redo(self):
		strs = []

		strs += self.script_fluent_models()
		#strs += self.script_fluent_udf()
		strs += self.script_fluent_materials()
		strs += self.script_fluent_cell_zones()
		strs += self.script_fluent_boundary_conditions()
		strs += self.script_fluent_solve()
		strs += self.script_fluent_export()
		
		#print strs
		str = "\n".join(strs)
		
		return str


#############################################################################

if __name__=="__main__":

	if len(sys.argv) < 2:
		logging.info("usage")
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		logging.info("file not found")
		sys.exit(1)

	case = Case(sys.argv[1])

	sys.exit(0)


