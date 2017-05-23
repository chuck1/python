



def zone_type(name, type):
	yield "/mesh/modify-zones/zone-type {0} {1}".format(
			name,
			type)
	

def cell_zone(name, type, material, energy, viscous):
	for s in zone_type(name, type): yield s

	if type == "fluid":
		for s in fluid(name, material, energy, viscous): yield s
	elif type == "solid":
		for s in solid(name, material, energy): yield s
	else:
		raise ValueError("bad cell zone type")


def fluid(name, material, energy, viscous):
	q_energy = "no no" if energy else ""
	
	if viscous == "laminar":
		q_viscous = ""
	elif viscous == "kw-standard":
		q_viscous = "no"
	else:
		raise ValueError("bad viscous {0}".format(viscous))


	ref_frame_origin = "no 0 no 0 no 0"
	ref_frame_compon = "no 0 no 0 no 1"
	
	yield "/define/boundary-conditions/fluid {0} yes {1} {2} no {3} {4} no no {5} no".format(
			name,
			material,
			q_energy,
			ref_frame_origin,
			ref_frame_compon,
			q_viscous)
	

def solid(name, material, energy):

	q_energy = "no no" if energy else ""
	
	ref_frame_origin = "no 0 no 0 no 0"
	ref_frame_compon = "no 0 no 0 no 1"
	
	yield "/define/boundary-conditions/solid {0} yes {1} {2} no {3} {4} no no".format(
			name,
			material,
			q_energy,
			ref_frame_origin,
			ref_frame_compon)

def mass_flow_inlet(name, energy, viscous, flow, temperature):
	
	if energy:
		q_energy = "no {0}".format(temperature)
	else:
		q_energy = ""
	
	if viscous == "kw-standard":
		q_kw = "no no yes 5 10"
	elif viscous == "laminar":
		q_kw = ""
	else:
		raise ValueError("bad viscous")
	
	
	# zone-type
	str = "/define/boundary-conditions/zone-type ~a mass-flow-inlet"
	
	yield "(resolve_name \"{0}\" \"{1}\")".format(str, name)
	

	# mass-flow-inlet
	str = "/define/boundary-conditions/mass-flow-inlet ~a yes yes no {0} {1} no 0 no yes {2}".format(flow, q_energy, q_kw)

	yield "(resolve_name \"{0}\" \"{1}\")".format(str, name)

def wall_heat_flux_const(name, heat_flux, material):

	#str = "/define/boundary-conditions/wall ~a 0 no 0 no no no {0} no no no no 1".format(heat_flux)

	str = "/define/boundary-conditions/zone-type ~a wall"
	
	yield "(resolve_name \"{0}\" \"{1}\")".format(str, name)

	#change wall material...

	str = "/define/boundary-conditions/wall ~a 0 no 0 yes {0} no no {1} no no 1".format(material, heat_flux)

	yield "(resolve_name \"{0}\" \"{1}\")".format(str, name)
	










