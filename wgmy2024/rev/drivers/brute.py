#!/usr/bin/env python3

from itertools import product

hex_charset = "0123456789abcdef"


def fnv_hash(a):
    x = 0x811C9DC5
    for i in a:
        x = (0x1000193 * (ord(i) ^ x)) & (2**32 - 1)
    return x


def to_hex_char(n):
    return ord(hex_charset[n & 0xF])


v6 = [ord("?")] * 32
a2 = b"C:\\Program Files"
a3 = b"?" * 32

v6[24] = to_hex_char(a2[0])
v6[10] = to_hex_char(a2[1])
v6[30] = to_hex_char(a2[2])
v6[9] = to_hex_char(a2[3])
v6[1] = to_hex_char(a2[4])
v6[17] = to_hex_char(a2[5])
v6[23] = to_hex_char(a2[6])
v6[25] = to_hex_char(a2[7])
v6[5] = to_hex_char(a2[8])
v6[20] = to_hex_char(a2[9])
v6[14] = to_hex_char(a2[10])
v6[8] = to_hex_char(a2[11])
v6[31] = to_hex_char(a2[12])
v6[6] = to_hex_char(a2[13])
v6[0] = to_hex_char(a2[14])
v6[3] = to_hex_char(a2[15])
v6[19] = to_hex_char(a2[3])
v6[21] = a3[21]
v6[4] = a3[4]
v6[2] = a3[2]
v6[22] = a3[22]
v6[29] = a3[29]
v6[11] = a3[11]
v6[13] = a3[13]
v6[27] = a3[27]
v6[12] = a3[12]
v6[7] = a3[7]
v6[15] = a3[15]
v6[28] = a3[28]
v6[18] = a3[18]
v6[26] = a3[26]
v6[16] = a3[16]

out = "".join([chr(i) for i in v6])
# print(out)
# print(out[16:])


def brute(target, incomplete):
    guess_template = ""
    count = 0
    for c in incomplete:
        if c == "?":
            guess_template += "{}"
            count += 1
        else:
            guess_template += c

    pmuts = product(hex_charset, repeat=count)

    for pmut in pmuts:
        guess = guess_template.format(*pmut)
        if guess == "52c3a1c260accb0b":
            print(pmut)
            return guess
        out = fnv_hash(guess)
        if out == target:
            return guess

    return incomplete


second_part = brute(0x7C8DB53D, out[16:])
if "?" in second_part:
    print("Failed to find the correct string")
    quit()

print("Second part:", second_part)

full_part = brute(0x3B1F48B6, out[:16] + second_part)

if "?" in full_part:
    print("Failed to find the correct string")
    quit()

print("Flag:", full_part)
