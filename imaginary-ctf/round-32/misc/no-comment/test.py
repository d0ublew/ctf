#!/usr/bin/env python3

from string import printable
# import pdb

# https://stackoverflow.com/questions/59482234/is-an-execstring-builtins-none-a-secure-way-to-execute-user-inpu

inp = [
    "#\r().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('ls')",
    "#\ra = 1",
]
code = []

for line in inp:
    assert line.isascii()
    code.append(line)

print(code)
for line in code:
    if line[0] != '#':  # Good code should have comments
        assert not any(x in line for x in printable)

# _MODULE_SOURCE_CODE = '\n'.join(code)
# pdb.set_trace()
exec('\n'.join(code), {'__builtins__': None}, {})
