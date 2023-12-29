# Notes

- `malloc()` empties out chunk+8 (tcachebin key field)
- double free detection is based on the tcachebin key field, if the key field is empty, we could free the chunk
- `malloc()` should return a 16-byte aligned memory address

## PROTECT_PTR and REVEAL_PTR

From <https://elixir.bootlin.com/glibc/glibc-2.35/source/malloc/malloc.c#L351>

```c
#define PROTECT_PTR(pos, ptr) \
  ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
#define REVEAL_PTR(ptr)  PROTECT_PTR (&ptr, ptr)
```

### One mangled pointer known

Given a mangled pointer, only the lower 36 bits are XOR-ed.

```text
b @ 0x56130b8332c0 = 0x56130b8332a0

mangled_b = 0x56166ab38a93
              ^^^
These bits are not mangled and are parts of the XOR key

0x56166ab38a93    0x56130b8332a0
     ^^^               ^^^
                       0x561 ^ 0x66a


0x56166ab38a93    0x56130b8332a0
        ^^^               ^^^
                          0x30b ^ 0xb38


0x56166ab38a93    0x56130b8332a0
           ^^^               ^^^
                             0x833 ^ 0xa93
```

```py
def reveal(ptr):
    mask = 0xfff << 36
    while mask:
        ptr ^= (ptr & mask) >> 12
        mask >>= 12
    return ptr


assert reveal(0x56166ab38a93) == 0x56130b8332a0
```
