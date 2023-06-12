#!/usr/bin/env python3

from base64 import b64decode

with open('./public.key') as f:
    data = ''.join([i.strip() for i in f.readlines()[1:-1]])

with open('./dump', 'wb') as f:
    f.write(b64decode(data))
