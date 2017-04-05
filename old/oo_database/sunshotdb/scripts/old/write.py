#!/usr/bin/env python3
import oodb
import sunshotdb

# Design
d = sunshotdb.models.Circular(oodb.util.get_next_id(oodb.ROOT))

d.data['D'] = 500e-6
d.data['width_wall'] = 500e-6
d.data['NT'] = 19
d.data['width'] = 0.02
d.data['length'] = 0.01
d.data['length_channel'] = 0.01
d.data['fluid_str'] = 'co2'

# Geo
g = sunshotdb.models.Geo(oodb.util.get_next_id(oodb.ROOT), d.id)

g.data['desc'] = "full design; halfed by symmetry"

# Simulation
o = sunshotdb.models.Simulation(oodb.util.get_next_id(oodb.ROOT), g.id)

print(d,d.id)
print(g,g.id)
print(o,o.id)

o.data['desc'] = 'sim#0030 conjugate fluent full design; low_risk_9 v1 adapt'
o.data['pressure_inlet'] = 2560.4028
o.data['pressure_channel_inlet'] = 988.31702
o.data['pressure_channel_outlet'] = 303.8226
o.data['pressure_outlet'] = 0.0
o.data['temperature_inlet'] = 773.15
o.data['temperature_outlet'] = 929.31
#o.data['temperature_channel_inlet'] = 
#o.data['temperature_channel_outlet'] = 
o.data['temperature_heated_awa'] = 1081.8920


d.resolve()

g.design = d
o.geo = g


d.test()
g.test()
o.test()


#oodb.util.save_to_next(oodb.ROOT, [g,o])



