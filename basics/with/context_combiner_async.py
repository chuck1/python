import asyncio
import functools

class A:
    def __init__(self): pass

    async def __aenter__(self):
        print('enter A')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print('exit A')

class B:
    def __init__(self, a): pass

    async def __aenter__(self):
        print('enter B')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print('exit B')

class Combiner:
    def create_iterators(self):
        
        for cls in self.class_ctors:
            yield g(cls)
    
    def _enter(self):
        for i in self.iters:
            yield next(i)

    async def __aenter__(self):
        print('combiner enter')

        async def g(c, *args):
            async with c(*args) as value:
                yield value

        self.it_a = g(A).__aiter__()
        a = await self.it_a.__anext__()

        self.it_b = g(B, a).__aiter__()
        b = await self.it_b.__anext__()

        return a, b

    async def __aexit__(self, exc_type, exc, tb):
        try:
            b = await self.it_b.__anext__()
        except StopAsyncIteration: pass
        try:
            a = await self.it_a.__anext__()
        except StopAsyncIteration: pass

        print('combiner exit')



from contextlib import contextmanager

@contextmanager
async def agen():
    async with Combiner() as (a, b):
        print('in combiner context', a, b)
        yield a, b

async def atest():
    async with Combiner() as (a, b):
        print('in combiner context', a, b)

    print('after with')
    
    async with agen() as (a, b):
        print('in agen context', a, b)

    print('after with')


loop = asyncio.get_event_loop()

loop.run_until_complete(atest())

print('script exit')










