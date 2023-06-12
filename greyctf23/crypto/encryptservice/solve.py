#!/usr/bin/env python3

from pwn import remote, xor  # type: ignore[import]

# enc(nonce, key) ^ pt = ct
# enc(nonce, key) ^ flag = enc_flag
# enc_flag ^ ct = pt ^ flag
# (pt ^ flag) ^ pt = flag

io = remote("34.124.157.94", 10590)

pt = b"grey" * 10

io.sendlineafter(b"(in hex format): ", pt.hex().encode())
result = io.recvall(timeout=2).decode().split("\n")

flag = bytes.fromhex(result[-2].split()[-1])

for i in range(256):
    ct = bytes.fromhex(result[i].split()[-1])
    if ct[:4] == flag[:4]:
        tmp = xor(ct, flag)
        flag = xor(tmp, pt)
        print(flag)
        break
