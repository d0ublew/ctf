# Alternative Solution

- use `blobrunner64` to run the shellcode
- use `x64dbg` to attach to `blobrunner64`
- go to the `threads` tab and find the thread id from `blobrunner64` output
- right click and go to thread entry
- set breakpoint
- go back to `blobrunner64` window and resume the thread
