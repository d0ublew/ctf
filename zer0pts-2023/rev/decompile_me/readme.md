# Solution

RC4 is symmetric encryption

```gdb
dump memory enc &dat (void*)&dat+0x80
break *main+142
run < enc
x/s $r14
```
