#!/usr/bin/env python3
import concurrent
import concurrent.futures
import asyncio
from functools import partial
import time

def func():
    print('in func')
    time.sleep(3)
    print('func complete')

def done_callback(proto, fut):
    print('compute done, send data')

    proto.transport.write('this is your computed data'.encode())

class ServerClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        
        print('run computation in executor')
        fut = self.loop.run_in_executor(None, func)
        fut.add_done_callback(partial(done_callback, self))

loop = asyncio.get_event_loop()

# Each client connection will create a new protocol instance

coro = loop.create_server(
        partial(ServerClientProtocol, loop),
        '127.0.0.1',
        11000)

server = loop.run_until_complete(coro)

with concurrent.futures.ProcessPoolExecutor() as executor:
    loop.set_default_executor(executor)
        
    #print(loop.run_in_executor(executor, func, i))

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()



