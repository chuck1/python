
import concurrent.futures
import asyncio


def func(i):
    print('task %i' % i)



loop = asyncio.get_event_loop()

with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in range(10):
        print(loop.run_in_executor(executor, func, i))

loop.close()


