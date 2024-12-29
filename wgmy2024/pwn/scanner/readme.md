# Solution

Security:
- PIE
- No stack canary

TL;DR
- We could read more than the size of chunk allocated for the image file content. Thus, we could read the `do_scan` function address and use it to calculate the ELF image base address (since PIE is enabled).
- There is a stack buffer overflow on the menu input which allows us to overwrite the return address.
- Luckily there is a `./flag.txt` string from the `do_help` function and we could use it as the first argument of `get_image` function and read out the flar.
