#!/usr/bin/env python3

import struct

salt = b"lARqpBuxfjrYtxRvJ7x64AnueWSj8ypfSqTYnZkd"
target = [37, 15, 6, 56, 55, 16, 60, 44, 47, 17, 71,
          41, 71, 27, 99, 66, 38, 104, 10, 6, 87, 42, 91, 42]

a = b"RheO5PB6mfL5N3YBH45e5XuCEaWpvWUFESqTYnZk"
b = struct.pack("QQ", 0x422b274624060720, 0x3f2a432354240505)
print(b.hex())

for i in range(len(target)):
    print(chr(target[i] ^ salt[i % len(salt)]), end='')

c = []
for i in range(len(b)):
    iVar1 = i // len(a)
    c.append(b[i] ^ a[i])

print(bytes(c).decode())
