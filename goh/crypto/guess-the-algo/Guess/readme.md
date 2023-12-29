- use gdb and break on `strcmp()` and get the answer: `aes-256-cfb`

```console
(gdb) break *main+332
Breakpoint 1 at 0x1335
(gdb) r
Starting program: /home/doublew/projects/ctf/goh/crypto/guess-the-algo/Guess/Algorithm.elf
Guess the algorithm (Example: camellia-256-cfb)
Text: Do not go where the path may lead, go instead where there is no path and leave a trail
Encrypted: mxU3s5J//oLWotoeJfjvNpe7InXZL7sF/KYwU/Xr9jqRMYksM7Hfy1RbubFqxu6UoTG89QjYVGw8geErRPCygZyYAfx2ZQ6nLcwn77vFtNPBQfEOHWI=
Guess what algorithm it use: idk

Breakpoint 1, 0x0000555555555335 in main ()
(gdb) x/s $rdi
0x7fffffffd4b0: "idk"
(gdb) x/s $rsi
0x7fffffffd4e0: "aes-256-cfb"
(gdb)
```

```
Guess the algorithm (Example: camellia-256-cfb)
Text: Do not go where the path may lead, go instead where there is no path and leave a trail
Encrypted: mxU3s5J//oLWotoeJfjvNpe7InXZL7sF/KYwU/Xr9jqRMYksM7Hfy1RbubFqxu6UoTG89QjYVGw8geErRPCygZyYAfx2ZQ6nLcwn77vFtNPBQfEOHWI=
Guess what algorithm it use: aes-256-cfb
key: LicielaWasHere
```
