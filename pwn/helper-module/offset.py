from pwn import *
from glob import glob
import os
from binascii import unhexlify

def offset(io):
    io.sendlineafter(b"> ", cyclic(0x1000))
    io.wait()

    core = io.corefile

    for file in glob("./core.*"):
        os.remove(file)

    fault = unhexlify(hex(core.fault_addr)[2:])
    return cyclic_find(fault[:4])
