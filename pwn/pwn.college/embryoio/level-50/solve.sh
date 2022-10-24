#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
sed = process(['/bin/sed', '-n', '/pwn.college{.*}/p'])
chall = process(['/challenge/embryoio_level50'], stdout=sed.stdin)
while True:
    try:
        print(sed.recvline().decode())
    except:
        break
sed.close()
chall.close()
EOF

ipython <<< "run /tmp/solve.py"
