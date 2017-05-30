#!/usr/bin/env python3.6

import time
import concurrent.futures
import asyncio
import functools
from functools import partial
import multiprocessing
import aiohttp

import protocol

async def client_ws(app):
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://localhost:8080/ws') as ws:
        print('connected') 

        app.ws = ws

        print('wait for message')
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    print('close')
                    await ws.close()
                    break
                else:
                    print('msg:', msg.data)
                    #await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print('closed')
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('error')
                break

class App(object): pass

app = App()

loop = asyncio.get_event_loop()

coro = loop.create_server(
        partial(protocol.EchoServerClientProtocol, app), 
        '127.0.0.1', 11000)

server = loop.run_until_complete(coro)


loop.run_until_complete(client_ws(app))

loop.run_forever()

print('closing loop')
loop.close()
print('loop closed')





