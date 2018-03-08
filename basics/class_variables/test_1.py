
class Foo:

    @classmethod
    def foo(cls):
        print(cls)

    @property
    @classmethod
    def b(cls):
        print(cls)
        return 1

Foo.foo()

print(Foo.b)


