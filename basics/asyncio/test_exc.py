
import asyncio

async def func():
    raise Exception()

loop = asyncio.get_event_loop()

loop.run_until_complete(func())



