#!/usr/bin/env python3

import server

server.cli_write('hello')

print('read')
b = server.cli_read()

print(b)

