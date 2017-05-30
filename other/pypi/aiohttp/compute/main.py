#!/usr/bin/env python3

from aiohttp import web
import aiohttp
from functools import partial
import protocol

async def handle(request):
    with open('page.html') as f:
        text = f.read()
    response = web.Response(body=text)
    response.content_type = 'text/html'
    return response

async def websocket_handler(request):
    print('websocket handler')

    app = request.app

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print('wait for message')
    async for msg in ws:
        print('msg', msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'get data':
                await app.client_compute.send('request data'.encode())
                pass
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                    ws.exception())

    return ws

async def on_startup(app):
    print('on startup')
    coro = app.loop.create_connection(
            partial(protocol.ClientProtocol),
            '127.0.0.1', 11000)
    
    #client = app.loop.run_until_complete(coro)
    transport, proto = await coro

    print(proto)

    app.client_compute = proto

app = web.Application()

app.on_startup.append(on_startup)

app.router.add_get('/', handle)
app.router.add_get('/ws', partial(websocket_handler))

web.run_app(app, port=8080)



