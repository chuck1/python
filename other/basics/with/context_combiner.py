import functools

class A:
    def __init__(self, _):pass

    def __enter__(self):
        print('enter A')
        return self

    def __exit__(self, exc_type, exc, tb):
        print('exit A')

class B:
    def __enter__(self):
        print('enter B')
        return self

    def __exit__(self, exc_type, exc, tb):
        print('exit B')

class C:
    def __enter__(self):
        print('enter C')
        return self

    def __exit__(self, exc_type, exc, tb):
        print('exit C')

class Combiner:
    def __init__(self, class_ctors):
        self.class_ctors = class_ctors
        self.iters = tuple(i for i in self.create_iterators())
        print(self.iters)

    def create_iterators(self):
        def g(c):
            with c() as value:
                yield value
        
        for cls in self.class_ctors:
            yield g(cls)
    
    def _enter(self):
        for i in self.iters:
            yield next(i)

    def __enter__(self):
        print('combiner enter')
        ctxs = tuple(self._enter())
        return ctxs

    def __exit__(self, exc_type, exc, tb):
        for i in reversed(self.iters):
            try:
                next(i)
            except StopIteration:
                pass

        print('combiner exit')


with Combiner((
    functools.partial(A, None), B, C)) as (a, b, c):
    print('in combiner context', a, b, c)


print('script exit')










