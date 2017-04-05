#!/usr/bin/env python3

import sys

import oodb
import oodb.gui.spreadsheet

import sunshotdb

s0 = 'oodb.class_util.designs'
s0 = 'sunshotdb.models.Simulation'

s1 = "'id', ('type',lambda x: str(type(x))), 'Re', 'desc', 'mdot'"

s1 = "'id', ('design',lambda s: s.geo.design), 'Re', "
s1 = "'receiver_efficiency', ('dp/L3', lambda x: x.get('dp') / x.get('length')**3)"
s1 = "'id', 'desc', 'width'"
s1 = "'id', 'desc', 'mass_flow_rate', 'pressure_drop'"


if __name__ == '__main__':
    app = oodb.gui.spreadsheet.Application(sys.argv)
    w = oodb.gui.spreadsheet.Window(s0,s1)
    sys.exit(app.exec_())

