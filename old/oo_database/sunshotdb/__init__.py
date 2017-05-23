
print(__file__)

import os
import sys

import oodb

def setglobals():
    oodb.NAME = 'sunshotdb'
    oodb.ROOT,_ = os.path.split(__file__)
    oodb.DB = oodb.Database()

setglobals()

#import sunshotdb.models




