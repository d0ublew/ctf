#!/usr/bin/env python3

import re
from warnings import catch_warnings

import gmpy

with open("./fakaka", "r") as f:
    obf = f.read()

obf = obf.replace(
    '[n for n in ().__class__.__base__.__subclasses__() if "rni" in n.__name__ and n.__name__ == n.__name__.lower()][0]',
    'catch_warnings')

obf_s = set(re.findall(r'".+?"', obf))

s_map = [(s, eval(s)) for s in obf_s]

for s, un_s in s_map:
    obf = obf.replace(s, f'"{un_s}"')

obf = obf.replace(
    'catch_warnings()._module.__builtins__.__getitem__("bytes").__dict__.__getitem__("fromhex")',
    "bytes.fromhex")

obf = obf.replace(
    'catch_warnings()._module.__builtins__.__getitem__("bytes"),',
    "")

obf_s = set(
    re.findall(
        r'bytes\.fromhex\(".+?"\)\.decode\(\)',
        obf))

s_map = [(s, eval(s)) for s in obf_s]

for s, un_s in s_map:
    obf = obf.replace(s, f'"{un_s}"')

obf = obf.replace(
    'catch_warnings()._module.__builtins__.__getitem__("globals")().__getitem__("inp")',
    "inp")

obf_s = set(
    re.findall(
        r'\d+\^\d+',
        obf))

s_map = [(s, eval(s)) for s in obf_s]

for s, un_s in s_map:
    obf = obf.replace(s, f'{un_s}')

obf = re.sub(
    r'\.__getitem__\((\d+)\)\.__pow__\((\d+)\).__eq__\((\d+)\)',
    r'[\1]**\2 == \3', obf)

obf = obf.split("\n")[:-1]

flag = bytearray(51)
for eq in obf:
    s = re.search(r"inp\[(\d+)\]\*\*(\d+) == (\d+)", eq)
    idx = int(s.group(1))
    exp = int(s.group(2))
    target = int(s.group(3))
    flag[idx] = int(gmpy.mpz(target).root(exp)[0])

print(flag)
