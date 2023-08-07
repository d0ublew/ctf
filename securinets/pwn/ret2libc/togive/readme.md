# Solution

## Brief

- similar to `one is enough`: overwriting `main`'s `ebp` lowest byte to `NULL` and hope that the new `ebp` value points to our input

## Complete

```asm
call gets  ; first arg is [ebp-0x58] <-- our input buffer address
...
lea esp, [ebp-0x8]
pop ecx
pop ebx
pop ebp
lea esp, [ecx-4]
ret
...
```

We could see that after our input is read, the esp is changed to point to
`[ebp-0x8]`. The value of `ecx` after `pop ecx` is equivalent to `ebp` due
to this instruction `lea esp, [ecx-4]`.

As can be seen we can not directly overwrite the saved eip ([ebp-0x4]) as
we would mess up the `ecx` which in disguise is act as the function's `ebp`

Stack layout after supplying input of 0x50 bytes

```text

AAAA
AAAA
...
AAAA
bbbb  <-- value that would be pop to `ecx`
cccc  <-- value that would be pop to `ebx`
```

As can be seen, with the input of 0x50 bytes, we reached just before the
future value of `ecx`. Since our input is retrieved using `gets` and it
reads until `\n` is sent, the `\n` is changed to be `\x00` by `gets` to ensure
our input is NULL terminated. Therefore, our input is actually 0x51 bytes.
This last byte (`\x00`) overwrites the lowest byte of future `ecx`.

From now on, I will refer future `ecx` as `true ebp`

Let's say that before our input is being read, we have the following state:

```text
input buffer address: 0xffffc7f0
true ebp            : 0xffffc860
```

We could see that if we overwrite the `true ebp` last byte with the `gets`
NULL byte, when the `main` function reaches `lea esp, [ecx-4]`, the `esp`
will now points to `0xffffc7fc`, and the function will return to whatever
is in `0xffffc7fc`. Since this address is overlaps with our input buffer,
we could control the value of this memory address to be our ROP chain

```text
0xffffc7f0: ret gadget          <-- ret slide
0xffffc7f4: ret gadget
0xffffc7f8: ret gadget
0xffffc7fc: ret gadget
0xffffc780: ret gadget
0xffffc800: ret gadget
0xffffc804: ret gadget
0xffffc808: ret gadget
0xffffc810: ret gadget
0xffffc814: ret gadget
0xffffc818: ret gadget
0xffffc81c: ret gadget
0xffffc820: ret gadget
0xffffc824: ret gadget
0xffffc828: puts@plt            <-- ret to puts to leak libc
0xffffc82c: clean up gadget     <-- to clean up puts argument
0xffffc830: puts@got.plt        <-- puts argument
0xffffc834: gets@plt            <-- ret to gets to build second ROP chain on bss
0xffffc838: stack pivot gadget  <-- pivot stack to bss
0xffffc840: bss                 <-- gets argument
```

We have approximately `1/16` chance to get the desired state of
`input buffer address` and `true ebp`.
