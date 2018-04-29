import asyncio
import enum
import os
import ctypes
import struct

libc = ctypes.cdll.LoadLibrary('libc.so.6')


fd = libc.inotify_init()

print('fd={}'.format(fd))

class Flags(enum.IntEnum):
    MODIFY = 0x00000002
    CREATE = 0x00000100
    DELETE = 0x00000200
    DELETE_SELF = 0x00000400
    IGNORED = 0x00008000
    ISDIR = 0x40000000
    @classmethod
    def parse1(cls, flags):
        parsed = []
        for flag in cls.__members__.values():
            if flag & flags:
                flags &= ~flag
                parsed.append(flag)
        return parsed, flags

    @classmethod
    def parse(cls, flags):
        return [flag for flag in cls.__members__.values() if flag & flags]

watchers = {}
watchers_rev = {}

watcher_flags = Flags.CREATE | Flags.DELETE
#watcher_flags |= Flags.MODIFY
watcher_flags |= Flags.DELETE_SELF
watcher_flags |= Flags.IGNORED

def add_watch(path):
    #print('add watch for', repr(path))
    wd = libc.inotify_add_watch(fd, path.encode('utf-8'), watcher_flags)
    watchers[wd] = path
    watchers_rev[path] = wd

def rm_watch(path):
    #print('remove watch for', repr(path))
    wd = watchers_rev[path]
    del watchers[wd]
    del watchers_rev[path]
    libc.inotify_add_watch(fd, wd)

def go(loop):
    add_watch('/home/crymal/docs')

    PREFIX = struct.Struct('iIII')
    
    f = os.fdopen(fd, 'rb')

    print('f={}'.format(f))

    def reader():
        b = f.read(PREFIX.size)
        assert len(b) == PREFIX.size
        #b = os.read(fd, PREFIX.size)
        wd, flags, cookie, length = PREFIX.unpack(b)
        #print(wd, flags, cookie, length)
        b = f.read(length)
        assert len(b) == length
        path = b.rstrip(b'\x00').decode('utf-8')
        flags_parsed, rem = Flags.parse1(flags)
        print('{:32} {:16} {}'.format(watchers[wd], path, (flags_parsed, rem)))
        
        mask = Flags.CREATE | Flags.ISDIR
        if (flags & mask) == mask:
            path = os.path.join(watchers[wd], path)
            add_watch(path)

        mask = Flags.DELETE | Flags.ISDIR
        if (flags & mask) == mask:
            path = os.path.join(watchers[wd], path)
            #rm_watch(path)

    loop.add_reader(fd, reader)
    
loop = asyncio.get_event_loop()

try:
    go(loop)
    loop.run_forever()
except KeyboardInterrupt: pass
finally:
    loop.remove_reader(fd)

loop.stop()
loop.close()


