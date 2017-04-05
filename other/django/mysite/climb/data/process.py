#!/usr/bin/env python

import csv
import json

def app(lst, v):
    for l in lst:
        c = len(set(l.items()) & set(v.items()))
        if (c == len(set(l.items()))) and (c == len(set(v.items()))):
            # dicts are identical
            return

    lst.append(v)

locations = []
areas     = []
walls     = []
routes    = []
pitches   = []
climbs    = []

def process(filename):
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
    
            print row
    
            if row[0]:
                app(locations, {'name':row[0]})
           
            # area
            if row[1]:
                d = {'name':row[1]}
    
                if row[0]:
                    d['location'] = row[0]
    
                app(areas, d)
            
            # wall
            if row[2]:
                d = {'name':row[2]}
    
                if row[0]:
                    d['location'] = row[0]
    
                if row[1]:
                    d['area'] = row[1]
    
                app(walls, d)
    
            # route
            if row[3]:
                d = {'name':row[3]}
    
                if row[0]:
                    d['location'] = row[0]
    
                if row[1]:
                    d['area'] = row[1]
    
                if row[2]:
                    d['wall'] = row[2]
    
                app(routes, d)
    
            # pitch
            if True: #row[4]:
                d = {'name':row[4]}
    
                if row[0]:
                    d['location'] = row[0]
    
                if row[1]:
                    d['area'] = row[1]
    
                if row[2]:
                    d['wall'] = row[2]
    
                if row[3]:
                    d['route'] = row[3]
    
                d['aka']    = row[5]
                d['grade']  = row[6]+row[7]
                d['aid']    = row[8]
                d['danger'] = row[9]
                d['page']   = row[10]
                d['book']   = row[11]
                d['stars']  = row[12].replace("\xc2\xab","a")
                d['notes']  = row[13]
                
                if len(row) < 15:
                    d['best ascent'] = ''
                    d['send?']  = ''
                else:
                    d['best ascent'] = row[14]
                    d['send?']  = row[15]
    
                app(pitches, d)
   
            if len(row) > 16:
                for i in range(16,29):
                    if row[i]:
                        d = {'date':row[i]}
                    
                        if row[0]:
                            d['location'] = row[0]
        
                        if row[1]:
                            d['area'] = row[1]
        
                        if row[2]:
                            d['wall'] = row[2]
        
                        if row[3]:
                            d['route'] = row[3]
        
                        d['pitch'] = row[4]
                       
                        app(climbs, d)
            
        
process('log.csv')
process('todo.csv')

if 0:
    print "\n".join(list(str(l) for l in locations))
    print "\n".join(list(str(l) for l in areas))
    print "\n".join(list(str(l) for l in walls))
    print "\n".join(list(str(l) for l in routes))
    print "\n".join(list(str(l) for l in pitches))
    print "\n".join(list(str(l) for l in climbs))

data = [locations, areas, walls, routes, pitches, climbs]

with open('data.json', 'w') as f:
    json.dump(data, f)








