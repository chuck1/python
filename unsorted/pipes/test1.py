#!/usr/bin/env python


import sys
import os

name = "/tmp/python_pipe_test"

if sys.argv[1] == 'w':
    try:
        os.mkfifo(name)
    except OSError:
        pass

    with open(name, 'w') as f:
        f.write(sys.argv[2])
elif sys.argv[1] == 'r':
    with open(name, 'r') as f:
        print f.read()



