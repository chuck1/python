import datetime
import json
import urllib.request


def compute_travel_time(src, dst):
    #return datetime.timedelta(minutes=30)
    
    # Disneyland
    # Universal+Studios+Hollywood4

    res = urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key=AIzaSyBC80p5F9tIuz19N6RZezYZ7I9JVBBQLJ8".format(
        src,
        dst))
    
    s = res.read().decode('utf-8')
    
    d = json.loads(s)

    seconds = 0

    for k,v in d.items():
        #print(k)
        pass

    for r in d['routes']:
        for k,v in r.items():
            #print(k)
            pass
        
        for leg in r['legs']:
            #print('leg')
            for k,v in leg.items():
                #print('  ',k)
                pass

    r = d['routes'][0]
    for leg in r['legs']:
        seconds += leg['duration']['value']
    
    return datetime.timedelta(seconds=seconds)

"""
represents traveling from one place to another or
plans to do so
"""
class Trip(object):
    def __init__(self, src, dst, leave=None, arrive=None):
        self.src = src
        self.dst = dst
        
        

        if (leave is not None) and (arrive is not None):
            raise RuntimeError()
        
        #if leave is not None:
        
        self.leave = datetime.datetime.now()

        self.arrive = self.leave + compute_travel_time(src, dst)
        
        print("Trip from",self.src,"to",self.dst,"arrive at",self.arrive)

"""
a task where you need to more an item from one place to another
"""
class Deliver(object):
    def __init__(object):
        pass
    


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

if __name__ == '__main__':
    Trip("Disneyland","Universal+Studios+Hollywood4")
    











