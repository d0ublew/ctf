#!/usr/bin/env python3

# type: ignore

import io
import struct

from qiling import Qiling
from qiling.const import QL_INTERCEPT, QL_VERBOSE
from qiling.os.const import BYTE, POINTER, SIZE_T, UINT
from qiling.os.mapper import QlFsMappedObject
from unicorn.x86_const import UC_X86_INS_CPUID


class FakeUrandom(QlFsMappedObject):

    def read(self, size: int) -> bytes:
        if size == 0x1:
            return b"\xff"
        return b"A" * size

    def fstat(self) -> int:
        return -1

    def close(self) -> int:
        return 0


def challenge1(ql: Qiling):
    ql.mem.map(addr=0x1000, size=0x1000, info="challenge 1")
    ql.mem.write_ptr(addr=0x1337, value=1337)


def challenge2(ql: Qiling):
    def my_uname(ql: Qiling):
        params = ql.os.resolve_fcall_params({'name': POINTER})
        name = params['name']
        sysname = name
        version = name + 0xc3
        ql.mem.string(sysname, "QilingOS")
        ql.mem.string(version, "ChallengeStart")
        ql.arch.regs.rax = 0
    ql.os.set_api('uname', my_uname, QL_INTERCEPT.EXIT)


def challenge3(ql: Qiling):
    ql.add_fs_mapper(r"/dev/urandom", FakeUrandom())

    def my_getrandom(ql: Qiling):
        params = ql.os.resolve_fcall_params(
            {'buf': POINTER, 'buflen': SIZE_T, 'flags': UINT})
        buf = params['buf']
        buflen = params['buflen']
        ql.mem.write(buf, b"A" * buflen)
        ql.arch.regs.rax = buflen
    ql.os.set_api('getrandom', my_getrandom, QL_INTERCEPT.CALL)


def challenge4(ql: Qiling):
    def callback(ql: Qiling):
        ql.arch.regs.write('eax', 0x1)
    ql.hook_address(callback, QILING_BASE + 0xe43)


def challenge5(ql: Qiling):
    # def callback(ql: Qiling):
    #     rax = ql.arch.regs.rax
    #     edx = ql.arch.regs.edx
    #     rbp = ql.arch.regs.rbp
    #     ql.mem.write_ptr(rbp + rax * 4 - 0x40, edx, size=4)

    # ql.hook_address(callback, QILING_BASE + 0xe99)

    def my_rand(ql: Qiling):
        ql.arch.regs.rax = 0
    ql.os.set_api('rand', my_rand, QL_INTERCEPT.CALL)


def challenge6(ql: Qiling):
    ql.patch(0xf18, b"\x90\x90", None)


def challenge7(ql: Qiling):
    def my_sleep(ql: Qiling):
        ql.arch.regs.rax = 0
    ql.os.set_api('sleep', my_sleep, QL_INTERCEPT.CALL)


def challenge8(ql: Qiling):
    def callback(ql: Qiling):
        MAGIC = 0x3DFCD6EA00000539
        magic_occurrences = ql.mem.search(ql.pack64(MAGIC))

        for candidate in magic_occurrences:
            addr = candidate - 0x8
            raw_data = ql.mem.read(addr, 0x18)
            random_data, _, _, target = struct.unpack("QIIQ", raw_data)
            if ql.mem.string(random_data) == "Random data":
                ql.mem.write(target, b"\x01")
    ql.hook_address(callback, QILING_BASE + 0xfb5)

    # def callback(ql: Qiling):
    #     global rax
    #     rax = ql.arch.regs.rax
    # ql.hook_address(callback, QILING_BASE + 0xf5a)

    # def callback(ql: Qiling):
    #     raw_data = ql.mem.read(rax, 0x18)
    #     random_data, leet, magic, addr = struct.unpack("QIIQ", raw_data)
    #     print(f"{random_data=:#x}, {leet=:#x}, {magic=:#x}, {addr=:#x}")
    #     ql.mem.write(addr, b"\x01")
    # ql.hook_address(callback, QILING_BASE + 0xfb5)

    # def callback(ql: Qiling):
    #     rdx = ql.arch.regs.rdx
    #     ql.mem.write(rdx, b"\x01")
    # ql.hook_address(callback, QILING_BASE + 0xfb1)


def challenge9(ql: Qiling):
    def my_tolower(ql: Qiling):
        params = ql.os.resolve_fcall_params({'c': BYTE})
        ql.arch.regs.rax = params['c']
    ql.os.set_api("tolower", my_tolower, QL_INTERCEPT.CALL)


def challenge10(ql: Qiling):
    def callback(ql: Qiling):
        ql.add_fs_mapper("/proc/self/cmdline", io.BytesIO(b'qilinglab'))
        # ql.add_fs_mapper("/proc/self/cmdline", "./fake_cmdline")
    ql.hook_address(callback, QILING_BASE + 0x10a4)


def challenge11(ql: Qiling):
    def callback(ql: Qiling):
        if ql.arch.regs.arch_pc < QILING_BASE or ql.arch.regs.arch_pc >= QILING_BASE + 0x2000:
            return (0, False)
        ql.arch.regs.rbx = 0x696C6951
        ql.arch.regs.rcx = 0x614C676E
        ql.arch.regs.rdx = 0x20202062
        # ql.arch.regs.arch_pc += 2
        # https://github.com/unicorn-engine/unicorn/blob/d4b92485b1a228fb003e1218e42f6c778c655809/include/unicorn/x86.h#L83
        return (0, True)
    ql.hook_insn(callback, UC_X86_INS_CPUID)


rax = 0
ql = Qiling(
    ['./qilinglab-x86_64'],
    './rootfs/x8664_linux',
    verbose=QL_VERBOSE.OFF)
QILING_BASE = int(ql.profile.get("OS64", "load_address"), 16)
challenge1(ql)
challenge2(ql)
challenge3(ql)
challenge4(ql)
challenge5(ql)
challenge6(ql)
challenge7(ql)
challenge8(ql)
challenge9(ql)
challenge10(ql)
challenge11(ql)
# ql.debugger = True
ql.run()
