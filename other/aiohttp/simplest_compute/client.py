#!/usr/bin/env python3

import socket

HOST = 'localhost'
PORT = 11000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send('hello'.encode())
    s.send('hello'.encode())
    s.send('hello'.encode())
    print(s.recv(1024))
    print(s.recv(1024))
    print(s.recv(1024))


