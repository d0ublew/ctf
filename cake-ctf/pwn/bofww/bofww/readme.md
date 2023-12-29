# Note

## std::string Internals

```c
struct string {
    char *ptr;
    unsigned long inline_size;
    union {
        char inline_string[0xf];
        unsigned long max_size;
    };
}
```
