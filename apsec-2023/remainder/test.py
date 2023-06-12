#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from binascii import unhexlify

mod = "b65db9b8db7980cf2f81bb716e2cf00dcdb7b520af25e5f067fd43fb0d110d2d"

n = bytes_to_long(unhexlify(mod))

p = 270526863986746948836471200136703749083
q = 304910705762802129688918107022147108247

e = 0x10001

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

with open('./message_xaa.enc', 'rb') as f:
    data = bytes_to_long(f.read().strip())
    print(long_to_bytes(pow(data, d, n)))

with open('./message_xab.enc', 'rb') as f:
    data = bytes_to_long(f.read().strip())
    print(long_to_bytes(pow(data, d, n)))

with open('./message_xac.enc', 'rb') as f:
    data = bytes_to_long(f.read().strip())
    print(long_to_bytes(pow(data, d, n)))
