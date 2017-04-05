#!/usr/bin/env python3
import oodb
import sunshotdb

# Design
d = sunshotdb.models.Circular(182)

d.data['D'] = 500e-6
d.data['width_wall'] = 500e-6
d.data['NT'] = 19
d.data['width'] = 0.02
d.data['length'] = 0.01
d.data['length_channel'] = 0.01
d.data['fluid_str'] = 'co2'

oodb.util.save_to_next(oodb.ROOT, [d])



