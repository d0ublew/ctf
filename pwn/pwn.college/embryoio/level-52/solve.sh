#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
cat = process(['/usr/bin/cat', '-'], stdout=PIPE)
cat.sendline(b'pfyrvfew')
chall = process(['/challenge/embryoio_level52'], stdin=cat.stdout)
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
print(chall.recvline().decode())
EOF

ipython <<< "run /tmp/solve.py"
