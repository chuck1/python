import asyncio

class Context:
    async def __aenter__(self):
        print('enter')
        return self
    async def __aexit__(self, _1, _2, _3):
        print('exit')

async def gen():
    async with Context() as c:
        print('yield')
        yield

async def smth():
    print('work begin')
    await asyncio.sleep(1)
    print('work done')

async def amain():

    g = gen()

    await g.__anext__()

    await smth()

    print('amain exit')

    # it appears that when this function exits, we return to gen() after the yield statement

if __name__=='__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(amain())

    print('close loop')

    loop.close()

