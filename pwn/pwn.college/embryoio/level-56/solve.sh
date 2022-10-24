#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level56', stdout=PIPE)
sed = Popen(['/usr/bin/sed', '-n', '/pwn.college{.*}/p'], stdin=chall.stdout)
sed.wait(timeout=1)
EOF

python /tmp/solve.py
