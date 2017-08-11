#!/usr/bin/env python3
import os
import datetime
import json
import urllib.parse
import urllib.request
import pipes
import pickle
from pprint import pprint

import mysocket

def debug_google_response(d):
    print('items')
    for k,v in d.items():
        print('  ',k)
        pass

    for r in d['routes']:
        print('route items')
        for k,v in r.items():
            print('  ',k,repr(str(v)[:32]))
            pass
        
        legs = r['legs']
        print('legs', len(legs))
        for leg in r['legs']:
            print('  leg items')
            for k,v in leg.items():
                print('  ',k,repr(str(v)[:32]))
                pass
            print()
           
            pprint(leg['duration_in_traffic'])

            for step in leg['steps']:
                print('step items')
                for k,v in step.items():
                    print('  ',k)
                break

            print('  steps')
            for step in leg['steps']:
                #print('      ',step['start_location'])
                print('      ',step['html_instructions'] if 'html_instructions' in step else None)
                if 'maneuver' in step:
                    print('        ',step['maneuver'])
    
    r = d['routes'][0]
    for leg in r['legs']:
        print(leg['duration'])

google_maps_api_key = open(os.path.join(os.environ['HOME'],'git','sysadmin','other_config','google_maps_api.txt')).read()[:-1]

def timestamp(dt):
    return (dt - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)) // datetime.timedelta(seconds=1)

def compute_travel_time(src, dst, leave, arrive):
    
    values = {
            'origin':src,
            'destination':dst,
            'key':google_maps_api_key}

    #values['traffic_model'] = 'pessimistic'

    if arrive is not None:
        values['arrival_time'] = timestamp(arrive)

    if leave is not None:
        values['departure_time'] = timestamp(leave)

    data = "&".join(["{}={}".format(k,v) for k,v in values.items()])

    url = "https://maps.googleapis.com/maps/api/directions/json?"+data

    #print('url',url)

    with urllib.request.urlopen(url) as res:
        s = res.read().decode('utf-8')
    
    d = json.loads(s)

    #debug_google_response(d)

    seconds = 0

    r = d['routes'][0]
    for leg in r['legs']:
        if 'duration_in_traffic' in leg:
            seconds += leg['duration_in_traffic']['value']
        else:
            seconds += leg['duration']['value']
    
    return datetime.timedelta(seconds=seconds)

def compute_travel_time_2(wp, leave, arrive):

    assert len(wp) > 1

    w1 = wp.pop(0)
    w2 = wp.pop(0)

    dur = compute_travel_time(w1, w2, leave, arrive)

    while(wp):
        w1 = w2
        w2 = wp.pop(0)
        dur += compute_travel_time(w1, w2, leave, arrive)

    return dur

class Status(object): pass

class Plan(object): pass

"""
represents traveling from one place to another or
plans to do so
"""
class Trip(object):
    def __init__(self, src, dst, leave=None, arrive=None):
        self.src = src
        self.dst = dst
        self.arrive = arrive
        self.leave = leave

        if (leave is not None) and (arrive is not None):
            raise RuntimeError()
        

        #print('Trip')
        #print('  src',self.src)
        #print('  dst',self.dst)

    def duration(self):
        return compute_travel_time(self.src, self.dst, self.leave, self.arrive)

class Task(object): pass

"""
a task where you need to more an item from one place to another
"""
class Deliver(Task):
    """
    a src of None implies that you have the item on you
    """
    def __init__(self, dst, src=None):
        self.dst = dst
        self.src = src

    def compare_to(self, trip):

        if (self.src == trip.src)and (self.dst == trip.src):
            print('remember to bring ...')
            return

        dur1 = trip.duration()

        wp2 = [trip.src]

        if self.src is not None:
            if self.src != trip.src:
                wp2.append(self.src)

        if self.dst != trip.dst:
            wp2.append(self.dst)

        wp2.append(trip.dst)

        dur2 = compute_travel_time_2(wp2, trip.leave, trip.arrive)

        print('dur1',dur1)
        print('dur2',dur2)
    
        print('will add {} travel time'.format(dur2-dur1))

#class Client(pipes.Client):
class Client(mysocket.Client):
    def __init__(self):
        #super(Client, self).__init__("/tmp/reminder_pipe_1", "/tmp/reminder_pipe_2")
        super(Client, self).__init__("", 6000)

#class Server(pipes.Server):
class Server(mysocket.Server):
    def __init__(self):
        #super(Server, self).__init__("/tmp/reminder_pipe_1", "/tmp/reminder_pipe_2")
        super(Server, self).__init__("", 6000)

        self.status = None
        self.tasks = list()

    def do_read(self, s, b):
        print('reminder server recieved:')
        o = pickle.loads(b)
        print(o)

        if isinstance(o, Task):
            print('which is a task')
            print('add to task list')
            self.tasks.append(o)

        if isinstance(o, Status):
            print('which is a status')
            print('status updated')
            self.status = o
            print('compare the new status to tasks:')
            for t in self.tasks:
                print(t)
                t.compare_to(o.o)

        if isinstance(o, Plan):
            print('which is a plan')

        # confirmation
        s.send('message recieved'.encode('utf-8'))


"""
types of interactions with program

input:
    tell it you are embarking on a trip right now
response:
    program tells you not to forget something
    program tells you to make a stop along the way


types of information we need to store

 * need to take something from somewhere to somewhere


"""



