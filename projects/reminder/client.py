#!/usr/bin/env python3

import reminder
import pickle

loc1 = "17920+SW+114th+Ave,+Tualatin,+OR+97062"
loc2 = "Kaiser+Permanente+Beaverton+Medical+Office"
loc3 = "Disneyland"
loc4 = "Universal+Studios+Hollywood4"
loc5 = "16234+SW+Oneill+Ct,+Portland,+OR+97223"

trip = reminder.Trip(loc1,loc2)

deliver = reminder.Deliver(loc5)

#deliver.compare_to(trip)

status = reminder.Status()
status.o = trip

c = reminder.Client()

c.write(pickle.dumps(deliver))
c.read()

c.write(pickle.dumps(status))
c.read()


