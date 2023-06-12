#!/usr/bin/env python3


import requests
import re

url = "http://34.124.157.94:5003/"

s = requests.session()

for i in range(1):
    r = s.get(url)
    print(re.findall(r'data:image/jpeg;base64,.+"'))
