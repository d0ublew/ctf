# Solution

Heap Layout:

+-------------+
|   name      |
+-------------+
|bee-movie.txt|
|FILE struct  |
+-------------+
|script.txt   |
|FILE struct  |
+-------------+

- We have a heap overflow on name and directly below the name memory address is a FILE struct which is opened in read mode. Hence, we could overwrite the `_IO_read_ptr` field with any address to gain arbitrary address read.
- We could leak libc addresses from the GOT since PIE is not enabled.
- We also have enough size to overflow into the second FILE struct, opened in write mode, and overwrite the `_IO_write_ptr` field with any address to gain arbitrary address write.
- We use this arbitrary address write to overwrite the stdout FILE struct vtable to call system
