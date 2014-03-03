import sys
import random

import memcache

memcache.SERVER_MAX_VALUE_LENGTH = 2 * 1024 * 1024

mc = memcache.Client(['127.0.0.1:17900'], debug=0,
                     server_max_value_length=2*1024*1024)

n = 1000000

names = ('file-{0}'.format(i) for i in xrange(n))

action = sys.argv[1] if len(sys.argv) > 1 else None
usage = ('usage: {0} '
         'put [fname fcontent]|'
         'delete [fname]|'
         'list [bucket]|'
         'getinfo [fname]|'
         'getcontent [fname]|'
         'putfile fpath [fname]').format(sys.argv[0])

if action == 'put':
    if len(sys.argv) == 4:
        fname, fcontent = sys.argv[2:4]
        print(fname, ':', mc.set(fname, fcontent))
    else:
        min_size = 5 * 1024
        max_size = 10 * 1024
        sizes = (random.randint(min_size, max_size) for _ in xrange(n))
        for fname, fsize in zip(names, sizes):
            fcontent = 'abc' * (fsize / 3)
            print(fname, ':', mc.set(fname, fcontent))
elif action == 'delete':
    fname = sys.argv[2] if len(sys.argv) == 3 else ''
    if fname:
        print(fname, ':', mc.delete(fname))
    else:
        for fname in names:
            print(fname, ':', mc.delete(fname))
elif action == 'list':
    bucket = sys.argv[2] if len(sys.argv) == 3 else ''
    print(bucket, ':', mc.get('@{0}'.format(bucket)))
elif action == 'getinfo':
    fname = sys.argv[2] if len(sys.argv) == 3 else ''
    if fname:
        print(fname, ':', mc.get('?{0}'.format(fname)))
    else:
        for fname in names:
            print(fname, ':', mc.get('?{0}'.format(fname)))
elif action == 'getcontent':
    fname = sys.argv[2] if len(sys.argv) == 3 else ''
    if fname:
        names = [fname]
        content = mc.get(fname)
        if content:
            with open(fname, 'wb') as f:
                f.write(content)
        print(fname, ':', len(content))
    else:
        for fname in names:
            content = mc.get(fname)
            if content:
                with open(fname, 'wb') as f:
                    f.write(content)
            print(fname, ':', len(content))
elif action == 'putfile':
    import os.path
    if len(sys.argv) > 2:
        fpath = sys.argv[2]
        if not os.path.isfile(fpath):
            print(usage)
            exit()
    else:
        print(usage)
        exit()
    if len(sys.argv) > 3:
        fname = sys.argv[3]
    else:
        fname = os.path.basename(fpath)
    with open(fpath, 'rb') as f:
        fcontent = f.read()
    print(fname, ':', mc.set(fname, fcontent))
else:
    print(usage)
