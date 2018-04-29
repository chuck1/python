#!/usr/bin/env python3
import datetime
import reminder
import pickle
import pytz

loc1 = "17920+SW+114th+Ave,+Tualatin,+OR+97062"
loc2 = "Madras,+OR+97741"

t = pytz.utc.localize(datetime.datetime.utcnow())

trip = reminder.Trip(loc1, loc2, leave=t)

s = trip.duration().total_seconds()

print('{},{}'.format(t.strftime('%Y-%m-%d %H:%M'),s))

