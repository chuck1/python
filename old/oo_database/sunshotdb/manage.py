#!/usr/bin/env python3
import os
import argparse
import readline
import code
import datetime
import shutil

import oodb
import sunshotdb


parser = argparse.ArgumentParser()
parser.add_argument("command")
args = parser.parse_args()




if args.command == "shell":
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()
elif args.command == "backup":
    print("ROOT",oodb.ROOT)
    src = os.path.join(oodb.ROOT, 'data')
    dtstr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    dst = os.path.join(oodb.ROOT, 'backup', dtstr)
    print("dst",dst)
    shutil.copytree(src,dst)
    
    

