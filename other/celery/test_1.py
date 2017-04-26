#!/usr/bin/env python3

import tasks
import pickle

if __name__=='__main__':

    print(tasks.add(2,2))
    
    print('apply_async')
    res = tasks.add.apply_async((2,2),countdown=3)
    
    print('res',repr(res))

    pickle.dumps(res)

    print('get')
    print(res.get())

    print('done')

