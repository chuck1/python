
import asyncio

async def f1(q):
    i = q.get_nowait()
    print('f1', i)
    q.task_done()
    print('f1 task_done')

async def f2(q):
    print('f2 join')
    await q.join()
    print('f2 joined')
    assert q.empty()

async def test(loop):
    q = asyncio.Queue()

    q.put_nowait('hello')

    print(q.qsize())

    done, pending = await asyncio.wait([
        loop.create_task(f2(q)), 
        loop.create_task(f1(q)),
        ])

    print(done)
    print(pending)




loop = asyncio.get_event_loop()

loop.run_until_complete(test(loop))


