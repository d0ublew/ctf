# Notes

```c
struct main.ShellStruct {
    uint64_t *shellcode;
    uint64_t unknown[2];
    uint64_t footer[3];
};
```

- `main.set_footer` get index input `i` and set `footer[i]` to our footer num input value
    does not check for index lower than 2
- `main.set_shellcode` set `*shellcode` to our input string
