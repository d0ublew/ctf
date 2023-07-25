# notes

- unable to write null bytes due to `strlen` check with return value of `read`
- `\n` causes the program to overwrite it with `\x00\x00`
- `[rbp-0x8]` is not cleared out after each loop
