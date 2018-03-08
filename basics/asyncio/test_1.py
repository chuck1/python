import time
import concurrent.futures
import asyncio


def func(i):
    print('task %i' % i)
    time.sleep(1)



loop = asyncio.get_event_loop()

with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in range(10):
        print(loop.run_in_executor(executor, func, i))
    print('exiting with statement')
    # the executor will block here until all threads are finished

print('closing loop')
loop.close()
print('loop closed')


