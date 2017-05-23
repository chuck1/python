from django.core.management.base import BaseCommand

from climb.models import Location
from climb.models import Area
from climb.models import Wall
from climb.models import Route
from climb.models import Pitch

import json

def dict_or_def(d,k):
    try:
        return d[k]
    except:
        return 'default'

def get_location(l):
    return Location.objects.get(name=l)

def get_area(l, a):
    return Area.objects.get(
            location=get_location(l),
            name=a)

def get_wall(l, a, w):
    return Wall.objects.get(
            area=get_area(l,a),
            name=w)

def get_route(l, a, w, r):
    return Route.objects.get(
            wall=get_wall(l,a,w),
            name=r)

def get_pitch(l, a, w, r, p):
    return Pitch.objects.get(
            route=get_route(l,a,w,r),
            name=r)

def load(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    locations = data[0]
    areas = data[1]
    walls = data[2]
    routes = data[3]
    pitches = data[4]
    
    for l in locations:
        print 'location', l
        loc = Location()
        loc.name = l['name']
        loc.save()

        area = Area()
        area.name = 'default'
        area.location = loc
        area.save()

        wall = Wall()
        wall.name = 'default'
        wall.area = area
        wall.save()
    
    for a in areas:
        print 'area', a
        area = Area()
        area.name = a['name']
        area.location = Location.objects.get(name=a['location'])
        area.save()

        wall = Wall()
        wall.name = 'default'
        wall.area = area
        wall.save()
    
    for w in walls:
        print 'wall', w
        wall = Wall()
        wall.name = w['name']
        wall.area = get_area(
                w['location'],
                dict_or_def(w,'area'))
        wall.save()
 
    for r in routes:
        print 'route', r
        route = Route()
        route.name = r['name']
        route.wall = get_wall(
                r['location'],
                dict_or_def(r,'area'),
                dict_or_def(r,'wall'))
        route.save()
 
    for p in pitches:
        print 'pitch', p
        pitch = Pitch()
        pitch.name = p['name']
        pitch.route = get_route(
                p['location'],
                dict_or_def(p,'area'),
                dict_or_def(p,'wall'),
                dict_or_def(p,'route'))
        pitch.save()
   
class Command(BaseCommand):
    help = 'load custom data file'

    #def add_arguments(self, parser):
    #    parser.add_arguments('file', nargs='1')

    def handle(self, *args, **options):
        if len(args) == 1:
            filename = args[0]
            print filename
            load(filename)
        else:
            return



