# read all objects into a single list

import pylab as pl

import oodb

db = oodb.DB()

g = oodb.class_util.designs

db.display(
    g,
    ['id', 'desc', ('type', type)])

