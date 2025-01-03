#!/usr/bin/env python3

# type: ignore

enc = {
    1: 74.0,
    2: 80.0,
    3: 87.0,
    4: 77.0,
    5: 76.0,
    6: 88.0,
    7: 80.0,
    8: 66.0,
    9: 82.0,
    10: 123.0,
    11: 87.0,
    12: 103.0,
    13: 52.0,
    14: 95.0,
    15: 97.0,
    16: 107.0,
    17: 52.0,
    18: 95.0,
    19: 101.0,
    20: 79.0,
    21: 52.0,
    22: 95.0,
    23: 79.0,
    24: 51.0,
    25: 117.0,
    26: 95.0,
    27: 115.0,
    28: 103.0,
    29: 89.0,
    30: 95.0,
    31: 50.0,
    32: 55.0,
    33: 52.0,
    34: 56.0,
    35: 57.0,
    36: 50.0,
    37: 55.0,
    38: 51.0,
    39: 125.0}

for k, v in enc.items():
    v = int(v)
    if (v > 90 and v < 97) or v > 122 or v < 65:
        print(chr(v), end='')
        continue
    if v >= 97:
        temp = (v - 97 - k) % 26
        print(chr(temp + 97), end='')
    else:
        temp = (v - 65 - k) % 26
        print(chr(temp + 65), end='')
