# Notes

```asm
0x7c00:      aaa
0x7c01:      adc    si,WORD PTR [bx]
0x7c03:      adc    ax,WORD PTR [bx+si]
0x7c05:      add    BYTE PTR [bx+si],al
0x7c07:      add    BYTE PTR [di],ch
0x7c09:      cli
0x7c0a:      xor    ax,ax
0x7c0c:      mov    ds,ax
0x7c0e:      mov    es,ax
0x7c10:      mov    ss,ax
0x7c12:      mov    sp,0xffff
0x7c15:      sti
0x7c16:      call   0x7c32   # get_offset
0x7c19:      cmp    al,0x1b  # ESC
0x7c1b:      je     0x7c30
0x7c1d:      sub    al,0x30
0x7c1f:      mov    ds:0x7c08,al
0x7c22:      call   0x7c37
0x7c25:      mov    eax,ds:0x7c04
0x7c29:      cmp    eax,DWORD PTR ds:0x7c00
0x7c2e:      jne    0x7c16
0x7c30:      jmp    0x7c30
0x7c32:      mov    ah,0x0
0x7c34:      int    0x16
0x7c36:      ret
0x7c37:      mov    ah,0x0
0x7c39:      int    0x16
0x7c3b:      cmp    ah,0x48
0x7c3e:      je     0x7c4b
0x7c40:      cmp    ah,0x50
0x7c43:      je     0x7c59
0x7c45:      cmp    al,0x1c
0x7c47:      je     0x7c16
0x7c49:      jmp    0x7c37
0x7c4b:      xor    ah,ah
0x7c4d:      mov    al,ds:0x7c08
0x7c50:      add    ax,0x7c04
0x7c53:      mov    bx,ax
0x7c55:      add    BYTE PTR [bx],0x1
0x7c58:      ret
0x7c59:      xor    ah,ah
0x7c5b:      mov    al,ds:0x7c08
0x7c5e:      add    ax,0x7c04
0x7c61:      mov    bx,ax
0x7c63:      sub    BYTE PTR [bx],0x1
0x7c66:      ret
```

## 16-bit mode in GDB

```sh
echo '<?xml version="1.0"?><!DOCTYPE target SYSTEM "gdb-target.dtd"><target><architecture>i8086</architecture><xi:include href="i386-32bit.xml"/></target>' > target.xml
wget https://raw.githubusercontent.com/qemu/qemu/master/gdb-xml/i386-32bit.xml
```

in gdb:

```console
(gdb) target remote :1234
(gdb) break *0x7c00
(gdb) set tdesc filename target.xml
```

## References

- <https://github.com/Dump-GUY/Malware-analysis-and-Reverse-engineering/blob/main/Debugging%20MBR%20-%20IDA%20+%20Bochs%20Emulator/Debugging%20MBR%20-%20IDA%20+%20Bochs%20Emulator.md>
- <https://stackoverflow.com/questions/32955887/how-to-disassemble-16-bit-x86-boot-sector-code-in-gdb-with-x-i-pc-it-gets-tr>
- <https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797>
- <https://en.wikipedia.org/wiki/INT_10H>
- <https://en.wikipedia.org/wiki/INT_16H>
- <https://stanislavs.org/helppc/scan_codes.html>
- <https://disasm.pro/>
