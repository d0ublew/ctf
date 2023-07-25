# note

Not sure why it does not work in non-debug mode (GDB)

```sh
gef-remote --qemu-user localhost 1234
```

## aarch64 (ARM64)

### Tools

References: <https://docs.pwntools.com/en/stable/qemu.html>

- gdb: <https://github.com/xpack-dev-tools/aarch64-none-elf-gcc-xpack/>
- qemu: `sudo apt-get install qemu-user-static`
- libs: `sudo apt-get install libc6-arm64-cross` installs to `/usr/aarch64-linux-gnu/`

Running qemu: `qemu-aarch64-static ./binary`

### Assembly

References: <http://blog.perfect.blue/ROPing-on-Aarch64>

#### Registers

- `x0` to `x7` are used to pass arguments
- `x29` is equivalent to `rbp` in `x86`
- `x30` stores return address

#### Function Prologue

Pre-indexed performs the offset operation then the assembly instruction:

- Add `N` to `sp` (`sp = sp + N`)
- Stores old frame pointer, `x29`, to `[sp]` and return address, `x30`, to `[sp + 8]`

```asm
stp x29, x30, [sp, #N]!  # pre-indexed [base, #offset]!
mov x29, sp
```

#### Function Epilogue

Post-indexed performs the assembly instruction then offset operation

- Load `[sp]` to `x29` and `[sp + 8]` to `x30`
- Add `N` to `sp` (`sp = sp + N`)

```asm
ldp x29, x30, [sp], #N  # post-indexed [base], #offset
```

#### Stack Layout

```text
+--------------------------+ ^ Lower memory address
| callee's saved x29       | |
+--------------------------+ |
| callee's saved x30       | |
+--------------------------+ | Stack growth direction
| callee's local variables |
+--------------------------+
| caller's saved x29       |
+--------------------------+
| caller's saved x30       |
+--------------------------+
| caller's local variables |
+--------------------------+   Higher memory address
```

Unlike in `x86` where saved `rbp` and `rip` are below the local variables which allow us to overwrite the saved `rip` and immediately return to our desired address,
in `ARM64` we overwrite the callers's return address instead due to the stack layout which means that we would first return normally to the caller and only then return to our desired address
