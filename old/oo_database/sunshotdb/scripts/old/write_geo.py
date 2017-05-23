# create a new object and add it to the database

import oodb

s = oodb.classes.Simulation(oodb.util.get_next_id())

oodb.util.save_to_next([s])

