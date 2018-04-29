
import asyncio

loop = asyncio.get_event_loop()

async def func1(f):
    return (await f)

async def test():
    f = loop.create_future()
    
    t = loop.create_task(func1(f))
    
    print(f)
    print(t)

    f.set_result(42)

    r = await t
    
    print(t.result())

    print(r)

    await t
    await t

    print(t)

loop.run_until_complete(test())




