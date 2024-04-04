#!/usr/bin/env python3

input_list = [
    4,
    54,
    41,
    0,
    112,
    32,
    25,
    49,
    33,
    3,
    0,
    0,
    57,
    32,
    108,
    23,
    48,
    4,
    9,
    70,
    7,
    110,
    36,
    8,
    108,
    7,
    49,
    10,
    4,
    86,
    43,
    59,
    124,
    86,
    0,
    69,
    59,
    47,
    93,
    78
]

key_str = "J"
key_str = "_" + key_str
key_str = key_str + "o"
key_str = key_str + "3"
key_str = "t" + key_str

key_list = [ord(char) for char in key_str]

while len(key_list) < len(input_list):
    key_list.extend(key_list)

result = [a ^ b for a, b in zip(input_list, key_list)]

result_text = ''.join(map(chr, result))
