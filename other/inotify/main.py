import asyncio
import aionotify
import os

# Setup the watcher
watcher = aionotify.Watcher()
watcher_flags = 0
#watcher_flags |= aionotify.Flags.MODIFY
#watcher_flags |= aionotify.Flags.ACCESS
#watcher_flags |= aionotify.Flags.ATTRIB
#watcher_flags |= aionotify.Flags.CLOSE_WRITE
#watcher_flags |= aionotify.Flags.CLOSE_NOWRITE
#watcher_flags |= aionotify.Flags.OPEN
#watcher_flags |= aionotify.Flags.MOVED_FROM
#watcher_flags |= aionotify.Flags.MOVED_TO
watcher_flags |= aionotify.Flags.CREATE 
watcher_flags |= aionotify.Flags.DELETE
watcher_flags |= aionotify.Flags.DELETE_SELF
#watcher_flags |= aionotify.Flags.MOVE_SELF
watcher.watch(path='/home/crymal/docs', flags=watcher_flags)

print(watcher_flags)

async def work():
    while True:
        # Pick the 10 first events
        event = await watcher.get_event()
        #if event.name[0]=='.': continue
        path, _ = watcher.requests[event.alias]
        event_path = os.path.join(path, event.name)
        print('{:32} {:16} {}'.format(path, event.name, aionotify.Flags.parse(event.flags)))
        
        mask = aionotify.Flags.CREATE | aionotify.Flags.ISDIR
        if (event.flags & mask) == mask:
            watcher.watch(path=event_path, flags=watcher_flags)

        #simulate waiting for other work
        #await asyncio.sleep(1)

# Prepare the loop
loop = asyncio.get_event_loop()

loop.run_until_complete(watcher.setup(loop))

task = loop.create_task(work())

try:
    loop.run_forever()
except: pass
finally:
    task.cancel()
    try:
        loop.run_until_complete(task)
    except: pass
    watcher.close()

loop.stop()
loop.close()

