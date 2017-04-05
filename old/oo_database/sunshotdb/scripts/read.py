#!/usr/bin/env python3

import oodb
import sunshotdb

#obj = list(oodb.DB.objects())

#l = lambda o: isinstance(o.geo.design, sunshotdb.models.PinFin)

#obj = list(oodb.DB.objects(objtype=sunshotdb.models.Simulation, tests=[l]))

#obj = list(oodb.DB.objects(objtype=sunshotdb.models.Rectangular))
obj = list(oodb.DB.objects())

for o in obj:
    #print(o, o.geo.design, o.__dict__)
    #print(o, o.get('PL'), o.get('Re'))
    #print(o, o.id, o.get('Re'), o.get('length'))
    #print(o, o.id, o.pod_to_data())
    #print(o, o.id, o.test())
    print(o, o.id)
    #print(o, o.id, o.get('width_channel'), o.get('height_channel'), o.get('desc'))
    pass



#oodb.DB.save()


