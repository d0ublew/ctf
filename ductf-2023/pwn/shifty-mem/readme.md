# Solution

Although the file descriptor has been closed and the file has been unlinked,
before this happens, if another program opens the file, this program could still
write to the file and the changes is reflected to the memory on the original
prorgam (maybe cause of `MAP_SHARED`)

Thus, we could create other two programs to perform race condition where the
first program set the `shm_req->len` value to be larger than `MAX_STR_LEN`
and another program to set the `shm_req->len` to be larger than 0 and smaller
than `MAX_STR_LEN`
