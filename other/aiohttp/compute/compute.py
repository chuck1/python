#!/usr/bin/env python3.6
import protocol

import asyncio

loop = asyncio.get_event_loop()

# Each client connection will create a new protocol instance

coro = loop.create_server(
        protocol.ServerClientProtocol,
        '127.0.0.1',
        11000)

server = loop.run_until_complete(coro)

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



