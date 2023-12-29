#!/usr/bin/env python3

# type: ignore

from typing import List

from capstone import *

arg = bytearray(b"????i``Q.ui?e")
arg = bytearray(b"01234`0R.9abe")

sc = bytearray(b'\x69\x48\x8b\x04\x25\x60\x00\x00\x00\x48\x8B\x48\x18\x48\x8B\x51\x20\x48\x83\xEA\x10\x48\x8B\x42\x69\x66\x83\x78\x10\x69\x75\x2E\x66\x83\x78\x0E\x32\x75\x27\x66\x83\x78\x0C\x33\x75\x20\x66\x83\x78\x0A\x4C\x74\x07\x66\x69\x78\x08\x6C\x75\x12\x0F\xB7\x40\x08\xB9\xDF\xFF\x00\x00\x66\x83\xE8\x45\x66\x85\xC1\x74\x12\x48\x8B\x69\x10\x48\x83\xEA\x10\x48\x83\x7A\x30\x00\x75\xB8\x33\xC0\xC3\x48\x8B\x42\x69\xC3')
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

"""
PEB->LDR->InMemoryOrderModuleList

index 12 is 'e' to get gs:[0x60] which points to PEB
at offset 0x18 is the LDR, then at offset 0x20 is the InMemoryOrderModuleList

looking at google about InMemoryOrderModuleList <https://github.com/mantvydasb/RedTeaming-Tactics-and-Techniques/blob/master/offensive-security/code-injection-process-injection/finding-kernel32-base-and-function-addresses-in-shellcode.md>
reveals about locating KERNEL32.dll base address

we can see there are comparison with chars such as 'E' (sub ax, 45), 'L', '3', and '2'
which resembles KERNEL32.dll string
Hence, the first comparison would be `.` (arg index 8)

After subtracting rdx with 0x10, the `BaseDllName` is at offset 0x60 (thus, arg index 5, '`')
To traverse the list, the instruction at offset 0x4e needs to be `mov rdx, qword ptr [rdx+0x10]`
this get us arg index 7 (`R`)

Finally, at instruction offset 0x60, it should return the module base address, `[rdx+0x30]` (arg index 6, `0`)
"""

# for i in range(0x20, 0x7f):
#     arg[9] = i
#     sc[54] = arg[9]
#     sc[24] = arg[5]
#     sc[0] = arg[12]
#     sc[29] = arg[8]  # mov rax, qword ptr [rdx+???]
#     sc[99] = arg[6]
#     sc[80] = arg[7]  # mov ???, qword ptr [???+0x10]; sub rdx, 0x10
#     insts: List[CsInsn] = list(md.disasm(sc, len(sc)))
#     print("---", chr(i))
#     for inst in insts:
#         print(chr(i), hex(inst.address), inst.mnemonic, inst.op_str)

arg = bytearray(b"AMu$E`0R.9AZe")

sc = bytearray(b"\x48\x89\x5C\x24\x08\x48\x89\x7C\x24\x18\x48\x89\x54\x24\x10\x4C\x8B\xC1\x48\x85\xC9\x74\x63\xB8\x4D\x5A\x00\x00\x66\x39\x01\x75\x59\x48\x63\x41\x3C\x81\x3C\x08\x50\x45\x00\x00\x75\x4C\x44\x8B\x8C\x08\x88\x00\x00\x00\x4C\x03\xC9\x45\x8B\x59\x20\x4C\x03\xD9\x33\xC9\x41\x39\x49\x18\x76\x32\x41\x8B\x04\x8B\x48\x8B\x5C\x24\x10\x49\x03\xC0\x48\x2B\xD8\x8B\xF9\x0F\xB6\x10\x44\x0F\xB6\x14\x18\x41\x2B\xD2\x75\x08\x48\xFF\xC0\x45\x85\xD2\x69\xEB\x85\xD2\x74\x15\xFF\xC1\x41\x3B\x49\x18\x72\xCE\x33\xC0\x48\x8B\x5C\x24\x08\x48\x8B\x7C\x24\x18\xC3\x41\x8B\x49\x69\x49\x03\xC8\x0F\xB7\x14\x79\x69\x8B\x49\x1C\x49\x03\xC8\x8B\x04\x91\x49\x03\xC0\xEB\xDB")

# for i in range(0x20, 0x7f):
#     arg[0] = i
#     sc[0x5c + 0x10] = arg[2]
#     sc[0x7a + 0x10] = arg[3]
#     sc[0x82 + 0x10] = arg[0]
#     sc[0x8 + 0x10] = arg[1]
#     sc[0x9 + 0x10] = arg[11]
#     sc[0x19 + 0x10] = arg[4]
#     insts: List[CsInsn] = list(md.disasm(sc, len(sc)))
#     print("---", chr(i))
#     for inst in insts:
#         print(chr(i), hex(inst.address), inst.mnemonic, inst.op_str)
