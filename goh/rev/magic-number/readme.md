- use any decompiler and notice there is a function named `calculateDynamicMagicNumber`
- use gdb, break on the function call, grab the magic number from the return value

```console
(gdb) break *main+37
Breakpoint 1 at 0x11fa
(gdb) run
Starting program: /home/doublew/projects/ctf/goh/rev/magic-number/secret.elf

Breakpoint 1, 0x00005555555551fa in main ()
(gdb) p $rax
$1 = 155333
(gdb) c
Continuing.
Enter the magic number to get the secret message: 155333
gohunikl2023{w0w_U_G3t_Me}
[Inferior 1 (process 9526) exited normally]
(gdb)
```
