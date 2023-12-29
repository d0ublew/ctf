#!/usr/bin/env python3

import RC6Encryption

# key = b"\xDA\xAD\x12\x60\x67\xC6\x8F\x1E\xC2\x9A\xEF\x46\xEF\xBE\xAD\xBA"

# with open("./maybe_rc6.bin", "rb") as f:
#     enc = f.read()


# rc6 = RC6Encryption.RC6Encryption(key, 20, 32, 5)

# for i in range(0, len(enc), 16):
#     print(rc6.blocks_to_data(rc6.decrypt(enc[i:i + 16])))


rc6 = RC6Encryption.RC6Encryption(b'abcdefghijklmnop', 12, 32, 5)
c = rc6.blocks_to_data(rc6.encrypt(b'abcdefghijklmnop'))
print(c)
rc6.blocks_to_data(rc6.decrypt(c))
