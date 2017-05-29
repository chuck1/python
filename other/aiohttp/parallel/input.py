#!/usr/bin/env python3

import socket

HOST = 'localhost'
PORT = 11000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(dir(s))
    while True:
        msg = input('enter message\n')
        s.send(msg.encode())



