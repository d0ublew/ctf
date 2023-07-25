#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes as l2b

with open("./private.pem", "r") as f:
    priv_key = RSA.import_key(f.read())

with open("./public.pem", "r") as f:
    pub_key = RSA.import_key(f.read())

with open("./flag.enc", "rb") as f:
    enc = f.read()


pt = pow(b2l(enc), priv_key.d, priv_key.n)
print(l2b(pt))
