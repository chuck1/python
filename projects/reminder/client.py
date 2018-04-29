#!/usr/bin/env python3
import datetime
import reminder
import pickle
import pytz

loc1 = "17920+SW+114th+Ave,+Tualatin,+OR+97062"
#loc1 = "17920 SW 114th+Ave, Tualatin, OR+97062"
loc2 = "Kaiser+Permanente+Beaverton+Medical+Office"
#loc2 = "Kaiser Permanente Beaverton Medical Office"
loc3 = "Disneyland"
loc4 = "Universal+Studios+Hollywood4"
loc5 = "16234+SW+Oneill+Ct,+Portland,+OR+97223"
loc6 = "Madras,+OR+97741"

tz = pytz.timezone('America/Los_Angeles')

#trip = reminder.Trip(loc1,loc2,arrive=datetime.datetime(2017, 4, 7, hour=16, tzinfo=tz))
trip = reminder.Trip(loc1, loc6, leave=pytz.utc.localize(datetime.datetime.utcnow()))

print(trip.duration())

#print(trip.duration())
#trip = reminder.Trip(loc1,loc2,leave=datetime.datetime(2017, 4, 8, hour=10, tzinfo=tz))
#print(trip.duration())
#trip = reminder.Trip(loc1,loc2,leave=datetime.datetime.now(tz=tz))
#print(trip.duration())

deliver = reminder.Deliver(loc5)

#deliver.compare_to(trip)

status = reminder.Status()
status.o = trip

if False:
    c = reminder.Client()

    c.write(pickle.dumps(deliver))
    c.read()

    c.write(pickle.dumps(status))
    c.read()


