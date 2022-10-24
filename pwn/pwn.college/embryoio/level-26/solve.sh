#!/bin/bash

FILE="/tmp/bexxuo"

cat << EOF > /tmp/solve.py
from pwn import *

with open('${FILE}', 'w+') as fd:
    fd.write('nrwpbsgf')
    fd.seek(0)
    r = process('/challenge/embryoio_level26', stdin=fd)
    while True:
        try:
            print(r.recvline().decode())
        except:
            break
EOF

python /tmp/solve.py | grep -oE "pwn.college{.*}"
