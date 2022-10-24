#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
grep = process(['/bin/grep', '-oE', 'pwn.college{.*}'])
chall = process(['/challenge/embryoio_level49'], stdout=grep.stdin)
while True:
    try:
        print(grep.recvline().decode())
    except:
        break
grep.close()
chall.close()
EOF

ipython <<< "run /tmp/solve.py"
