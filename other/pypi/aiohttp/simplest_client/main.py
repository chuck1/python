#!/usr/bin/env python3

from aiohttp import web
import aiohttp

async def handle(request):
    with open('page.html') as f:
        text = f.read()
    response = web.Response(body=text)
    response.content_type = 'text/html'
    return response

async def websocket_handler(request):
    print('websocket handler')
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print('wait for message')
    async for msg in ws:
        print('msg', msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                    ws.exception())

            print('websocket connection closed')

    return ws

app = web.Application()

app.router.add_get('/', handle)
app.router.add_get('/ws', websocket_handler)

web.run_app(app, port=8080)



