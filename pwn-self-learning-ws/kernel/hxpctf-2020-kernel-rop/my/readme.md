# Note

`KASLR` lowest 20 bits are not randomized. (?)

- `_text` until `__x86_retpoline_r15` is not affected by `FG-KASLR`
- `e_text`
