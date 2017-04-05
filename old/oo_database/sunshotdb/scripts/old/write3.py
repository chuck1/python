#!/usr/bin/env python3
import oodb
import sunshotdb

# Design
d = sunshotdb.models.Rectangular(oodb.util.get_next_id(oodb.ROOT))

d.data['des'] = 'first ms design'
d.data['width_channel'] = 100e-6
d.data['height_channel'] = 100e-6
d.data['width_wall'] = 100e-6
d.data['NT'] = 50
d.data['width'] = 0.01
d.data['length'] = 0.01
d.data['length_channel'] = 0.01
d.data['fluid_str'] = 'ms1'

# Geo
g = sunshotdb.models.Geo(oodb.util.get_next_id(oodb.ROOT), d.id)

g.data['desc'] = "full design"

# Simulation
o = sunshotdb.models.Simulation(oodb.util.get_next_id(oodb.ROOT), g.id)

print(d,d.id)
print(g,g.id)
print(o,o.id)

o.data['desc'] = 'conjugate; full design; maybe sim#0005'
o.data['pressure_inlet'] = 5e4
#o.data['pressure_channel_inlet'] = 
#o.data['pressure_channel_outlet'] = 
o.data['pressure_outlet'] = 0.0
o.data['temperature_inlet'] = 573.15
o.data['temperature_outlet'] = 873.15
#o.data['temperature_channel_inlet'] = 
#o.data['temperature_channel_outlet'] = 
o.data['temperature_heated_awa'] = 814


d.resolve()

g.design = d
o.geo = g


d.test()
g.test()
o.test()


#oodb.util.save_to_next(oodb.ROOT, [d,g,o])



