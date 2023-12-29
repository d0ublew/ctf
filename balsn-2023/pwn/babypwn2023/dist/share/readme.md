# Solution

Use leftover stack data from `puts()` which has I/O struct addresses for stack
pivoting, in this scenario, it pivots to `_IO_2_1_stderr_` and then overwrite
the `_IO_2_1_stdout_` struct to leak memory.
