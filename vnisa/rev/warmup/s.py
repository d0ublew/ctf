#!/usr/bin/env python3

from binascii import unhexlify

fns = b"63d82432bc76"
target = b"`\xe0\xe4\x2d\xff\x97\xdd\x13\xee\xa0\x55\xf4"
tnf = b"ccccccdddddd"

# v13 = []

# for i in range(256):
#     v13.append(i)


# v5 = 0

# for j in range(256):
#     a = v13[j] + v5
#     v12 = len(fns)
#     v5 = (fns[j % v12] + a) % 256
#     tmp = v13[j]
#     v13[j] = v13[v5]
#     v13[v5] = tmp

arr2 = [
    "D2B372000A353161",
    "BB273B7E3C14C256",
    "B97C7678AB75D917",
    "BC6B2810221DAA5E",
    "30AF7394747B093E",
    "553D8F827111665A",
    "8D41D1682B8BB419",
    "B7B2F40DC75BA3EC",
    "D4575297696220C4",
    "1F6FEE37A716C84C",
    "AD5905BF49DF08A2",
    "03D3A9448E509A6D",
    "21921EF736676307",
    "5C2C4590CF1B8C01",
    "95798A9E810ED091",
    "465FBDFA255129CA",
    "E064BE9FE5FF7D2D",
    "FE23B0A6A443B8FB",
    "40589887E8FD996E",
    "9D2AD86AD68602C9",
    "4B831ABAC5F6B133",
    "5DCE39D58865B5A1",
    "42AE06C1A8F8D7EF",
    "EB32DDF024E12E96",
    "8548139BC00CA515",
    "1C77CC4F4DE460E6",
    "7FE34A89DE38A047",
    "DA9CE97A3AF380DC",
    "043453CDFC26CBB6",
    "EDF1706C2FF5E284",
    "F2E79312EA0F4EDB",
    "AC0B3FC654C3F918",
    "0000472CD5E94C61",
]
for i in range(len(arr2)):
    arr2[i] = unhexlify(arr2[i])[::-1]

arr2 = b"".join(arr2)
v13 = bytearray(arr2)
arr = []

v7 = 0
v6 = 0
for k in range(len(tnf)):
    v6 = (v13[v7] + v6) % 256
    v7 += 1
    tmp = v13[v7]
    v13[v7] = v13[v6]
    v13[v6] = tmp
    v3 = tnf[k]
    arr.append(v13[(v13[v6] + v13[v7]) % 256] ^ v3)

print(bytes(arr).hex())
