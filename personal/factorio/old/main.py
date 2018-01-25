
class TransportObject:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

transport_objects = {}

def add_transport_object(name, rate):
    transport_objects[name] = TransportObject(name, rate)

add_transport_object("express transport belt", 40.0)
add_transport_object("stack inserter", 12.41)

