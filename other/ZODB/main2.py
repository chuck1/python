import datetime
from lxml import etree
import persistent

class Serializable(object):

class Test(persistent.Persistent, Serializable):
    def __init__(self):
        self.time = str(datetime.datetime.now())

t = Test()

t._serialize()



