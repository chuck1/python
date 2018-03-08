import asyncio
import concurrent.futures

async def func():
    print('func')
    i = 0
    while True:
        print(i)
        i += 1
        await asyncio.sleep(1)


async def test(loop):

    task = loop.create_task(func())

    #await asyncio.sleep(3)

    task.cancel()

    if False:
        try:
            await task
        except concurrent.futures.CancelledError:
            print('cancelled')


loop = asyncio.get_event_loop()

loop.run_until_complete(test(loop))

loop.close()


