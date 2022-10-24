#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
cat = process(['/bin/cat', '-'])
chall = process(['/challenge/embryoio_level48'], stdout=cat.stdin)
while True:
    try:
        print(cat.recvline().decode())
    except:
        break
cat.close()
chall.close()
EOF

ipython <<< "run /tmp/solve.py"
