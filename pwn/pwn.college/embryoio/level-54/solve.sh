#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level54', stdout=PIPE)
cat = Popen('/usr/bin/cat', stdin=chall.stdout)
cat.wait(timeout=1)
EOF

python /tmp/solve.py
