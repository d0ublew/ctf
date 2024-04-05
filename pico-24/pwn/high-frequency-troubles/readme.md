# Notes

```sh
objdump -t ./libc.so.6 | rg -e '\.tdata' -e '\.tbss' | rg '\bl\b' sort -k1

readelf -T -s ./libc.so.6 | rg 'TLS' | rg 'LOCAL' | sort -k2
```
