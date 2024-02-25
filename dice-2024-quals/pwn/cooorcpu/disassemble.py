#!/usr/bin/env python3

import binascii
import struct

with open("./system_rom.rom", "rb") as f:
    mem = b"".join(f.read().split(b"\n"))
    mem = binascii.unhexlify(mem)


class Enc:
    def __init__(self) -> None:
        self.opcode = (0, 6)
        self.rd = (-1, -1)
        self.funct3 = (-1, -1)
        self.rs1 = (-1, -1)
        self.rs2 = (-1, -1)
        self.funct7 = (-1, -1)
        self.imm: list = []


class Insn:
    def __init__(self, name, enc: Enc, unit) -> None:
        self.name = name
        self.enc: Enc = enc
        self.unit = unit
        self.text = ""
        self.rd = -1
        self.func3 = -1
        self.rs1 = -1
        self.rs2 = -1
        self.funct7 = -1
        self.imm = -1

    def parse(self, raw: bytes):
        num = (struct.unpack("<I", raw)[0])
        self.rd = self.slice(num, self.enc.rd)
        self.funct3 = self.slice(num, self.enc.funct3)
        self.rs1 = self.slice(num, self.enc.rs1)
        self.rs2 = self.slice(num, self.enc.rs2)
        self.funct7 = self.slice(num, self.enc.funct7)
        if len(self.enc.imm) > 0:
            self.imm = 0
            for imm in self.enc.imm:
                tmp = self.slice(num, imm[0])
                self.imm = self.imm | (tmp << imm[1][0])

    def decode(self, raw: bytes):
        self.parse(raw)
        self.text = f"{self.unit:<4} {self.name:<10}"
        self.text += f" rd:{self.rd:>8}"
        self.text += f" funct3:{self.funct3:>4}"
        self.text += f" rs1:{self.rs1:>7}"
        self.text += f" rs2:{self.rs2:>7}"
        self.text += f" funct7:{self.funct7:>4}"
        self.text += f" imm:{self.imm:>7}"

    def slice(self, num, indices: tuple[int, int]):
        if indices[0] == -1:
            return -1
        delta = (indices[1] - indices[0]) + 1
        return (num >> indices[0]) & (2**delta - 1)


class R(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.rd = (7, 11)
        self.funct3 = (12, 14)
        self.rs1 = (15, 19)
        self.rs2 = (20, 24)
        self.funct7 = (25, 31)


class I(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.rd = (7, 11)
        self.funct3 = (12, 14)
        self.rs1 = (15, 19)
        self.imm = [
            ((20, 31), (0, 11)),
        ]


class U(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.rd = (7, 11)
        self.funct3 = (12, 14)
        self.rs1 = (15, 19)
        self.imm = [
            ((20, 31), (0, 11))
        ]


class B(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.funct3 = (12, 14)
        self.rs1 = (15, 19)
        self.rs2 = (20, 24)
        self.imm = [
            ((7, 7), (11, 11)),
            ((8, 11), (1, 4)),
            ((25, 30), (5, 10)),
            ((31, 31), (12, 12)),
        ]


class J(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.rd = (7, 11)
        self.imm = [
            ((12, 19), (12, 19)),
            ((20, 20), (11, 11)),
            ((21, 30), (1, 10)),
            ((31, 31), (20, 20)),
        ]


class S(Enc):
    def __init__(self) -> None:
        super().__init__()
        self.funct3 = (12, 14)
        self.rs1 = (15, 19)
        self.rs2 = (20, 24)
        self.imm = [
            ((7, 11), (0, 4)),
            ((25, 31), (5, 11)),
        ]


class ARITH(Insn):
    def __init__(self) -> None:
        super().__init__("ARITH", R(), "ALU")


class ARITH_IMM(Insn):
    def __init__(self) -> None:
        super().__init__("ARITH_IMM", I(), "ALU")

    def decode(self, raw):
        super().parse(raw)
        self.text += f"{self.unit:<4} "
        if (self.funct3, self.funct7) == (0, -1):
            self.text += f"ADD x{self.rd}, x{self.rs1}, {self.imm}"
        if (self.funct3, self.funct7) == (4, -1):
            self.text += f"XOR x{self.rd}, x{self.rs1}, {self.imm}"
        if (self.funct3, self.funct7) == (6, -1):
            self.text += f"OR x{self.rd}, x{self.rs1}, {self.imm}"
        if (self.funct3, self.funct7) == (7, -1):
            self.text += f"AND x{self.rd}, x{self.rs1}, {self.imm}"


class LUI(Insn):
    def __init__(self) -> None:
        super().__init__("LUI", U(), "ALU")


class BRANCH(Insn):
    def __init__(self) -> None:
        super().__init__("BRANCH", B(), "BU")


class JAL(Insn):
    def __init__(self) -> None:
        super().__init__("JAL", J(), "BU")


class JALR(Insn):
    def __init__(self) -> None:
        super().__init__("JALR", I(), "BU")


class LOAD(Insn):
    def __init__(self) -> None:
        super().__init__("LOAD", I(), "LSU")


class STORE(Insn):
    def __init__(self) -> None:
        super().__init__("STORE", S(), "LSU")

    def decode(self, raw):
        super().parse(raw)
        self.text += f"{self.unit:<4} "
        self.text += f"STORE [x{self.rs1}+{self.imm}], x{self.rs2}"


class AUIPC(Insn):
    def __init__(self) -> None:
        super().__init__("AUIPC", U(), "BU")


class ECALL(Insn):
    def __init__(self) -> None:
        super().__init__("ECALL", I(), "BU")


class ERET(Insn):
    def __init__(self) -> None:
        super().__init__("ERET", J(), "BU")


class SETPRIV(Insn):
    def __init__(self) -> None:
        super().__init__("SETPRIV", R(), "PU")


class FLAG(Insn):
    def __init__(self) -> None:
        super().__init__("FLAG", U(), "IOU")


class WELCOME(Insn):
    def __init__(self) -> None:
        super().__init__("WELCOME", U(), "IOU")


OPCODES = {
    0b0110011: ARITH,
    0b0010011: ARITH_IMM,
    0b0110111: LUI,
    0b1100011: BRANCH,
    0b1101111: JAL,
    0b1100111: JALR,
    0b0000011: LOAD,
    0b0100011: STORE,
    0b0010111: AUIPC,
    0b1110011: ECALL,
    0b1110010: ERET,
    0b0110100: SETPRIV,
    0b1110000: FLAG,
    0b1110001: WELCOME,
}


def disassemble(raw: bytes):
    num = (struct.unpack("<I", raw)[0])
    opcode = num & (2**7 - 1)
    insn: Insn = OPCODES[opcode]()
    insn.decode(raw)
    print(insn.text)


i = 0
while i < len(mem):
    disassemble(mem[i:i + 4])
    i += 4
