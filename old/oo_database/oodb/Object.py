import sys
import logging
import inspect

import oodb



class Object:
    def __init__(self, i):
        self.id = i
        self.data = {}

    def print_dict(self):
        print('__dict__:')
        for k,v in self.__dict__.items():
            print("{:16}{!s:16}".format(k,v))
        print('data:')
        for k,v in self.data.items():
            print("{:16}{!s:16}".format(k,v))

    def get(self, name):
        #logging.info('get')

        try:
            a = self.data[name]
        except:
            try:
                a = getattr(self, name)
            except AttributeError as err:
                self.print_dict()
                raise err

        if inspect.ismethod(a):
            #logging.info('method', a())
            return a()
        else:
            #logging.info('not method')
            return a

    def has(self, name):
        if name in self.data:
            return True
        
        return hasattr(self, name)

    def pod_to_data(self):

        if not hasattr(self, 'data'):
            self.data = {}

        d = dict(self.__dict__)
        for k,v in d.items():
            if isinstance(v, str):
                print("str",k,v)
                self.data[k] = v
                delattr(self, k)
            if isinstance(v, float):
                print("float",k,v)
                self.data[k] = v
                delattr(self, k)
            if isinstance(v, int):
                if k == 'id':
                    print("int",k,v)
                    self.data[k] = v
                    delattr(self, k)


