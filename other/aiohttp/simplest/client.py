#!/usr/bin/env python3.6

import asyncio
import aiohttp

async def client_ws():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://localhost:8080/ws') as ws:

        await ws.send_str('Hello')

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    print('close')
                    await ws.close()
                    break
                else:
                    print('msg')
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print('closed')
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('error')
                break
    

loop = asyncio.get_event_loop()
loop.run_until_complete(client_ws())
loop.close()

