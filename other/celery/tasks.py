#!/usr/bin/env python3

import celery

app = celery.Celery(backend='rpc',broker='amqp://guest@localhost/host1')

print(app)

@app.task
def add(x,y):
    return x+y

print(add)
print(add.name)


