#!/usr/bin/env python3

from aiohttp import web

async def handle(request):

    await request.post()

    print('post =', request.POST)

    msg = ''

    response = web.Response(text='received: ' + msg)
    return response

app = web.Application()

app.router.add_post('/sms', handle)

web.run_app(app)


