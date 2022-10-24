#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
rev = process(['/usr/bin/rev'] )
chall = process(['/challenge/embryoio_level51'], stdout=rev.stdin)
while True:
    try:
        print(rev.recvline().decode())
    except:
        break
rev.close()
chall.close()
EOF

ipython <<< "run /tmp/solve.py"
