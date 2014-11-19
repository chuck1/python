#!/usr/bin/env python3

import oodb
import sunshotdb

#obj = list(oodb.DB.objects())

l = lambda o: isinstance(o.geo.design, sunshotdb.models.PinFin)

obj = list(oodb.DB.objects(objtype=sunshotdb.models.Simulation, tests=[l]))

for o in obj:
    print(o, o.geo.design, o.__dict__)
    pass


