# Solution

- arbitrary write primitive on `updateConfig` which allows writing into memory address larger than `config` (`[elf_base+0x0000000000004060]`)
- arbitrary file read via `readChat` to read `/proc/self/maps` to leak `PIE` and `ASLR`
- Setting config index 2 with `backup: 1` allow us to call `backupCall`
- `backupCode` is mapped with `rwx` permissions
- use arbitrary write primitive to write shellcode on `backupCode` memory address and set `backupCall` to point to `backupCode`
