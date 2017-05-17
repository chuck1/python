import sys
import datetime
import persistent

import MyItemDatabase.application
import MyItemDatabase.model
import MyItemDatabase.util

def startup(app):
    
    e = MyItemDatabase.model.ElectronicExpansionValveSporlan()
    
    e.pipeConnectionInlet  = MyItemDatabase.util.PipeConnection(MyItemDatabase.util.PipeSize(0.75), "ODF")
    e.pipeConnectionOutlet = MyItemDatabase.util.PipeConnection(MyItemDatabase.util.PipeSize(1.00), "ODF")

    app.root.itemManager.add(e)
    
    app.commit()    

app = MyItemDatabase.application.Application()

startup(app)

for k,v in app.root.itemManager.tree.items():
    print k,v



