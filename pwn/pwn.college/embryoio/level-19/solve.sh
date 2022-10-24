#!/bin/bash

FILE="/tmp/uoxycb"

cat << EOF > /tmp/solve.py
from pwn import *

with open('${FILE}', 'w+') as fd:
    fd.write('nfajblnd')
    fd.seek(0)
    r = process('/challenge/embryoio_level19', stdin=fd)
    while True:
        try:
            print(r.recvline().decode())
        except:
            break
EOF

ipython <<< "run /tmp/solve.py" | grep -oE "pwn.college{.*}"
