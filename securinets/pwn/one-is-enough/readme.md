# Note

- off-by-one error in `readInput`, `readInput(addr, size)` sets `[addr+size+1]` to `NULL` if the given input is exactly `size` bytes long
    impact: overwrites `main`'s' `rbp` lowest byte to `NULL` and hope that the new `rbp` value points to our input
