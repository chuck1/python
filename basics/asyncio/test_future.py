import asyncio



loop = asyncio.get_event_loop()

async def func1(f):
    return (await f)

async def test():
    f = loop.create_future()
    
    t = loop.create_task(func1(f))

    t.cancel()

    try:
        await t
    except:
        pass

    print('f cancelled', f.cancelled())


loop.run_until_complete(test())



