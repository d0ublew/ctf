import base64

enc = "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"

dec = base64.b64decode(enc)
with open("out", "wb") as f:

    for i in range(len(dec)):
        f.write(dec[i] ^ 256)