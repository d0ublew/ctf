# Notes

```python
def fak():
    global g
    lsb = g & 1
    g = g >> 1 # g//2
    if lsb == 1:
        xor_value = 0x80200003
        g = g ^ xor_value
    return chr(g & 0xff)

v_42 = 1
g = 0x3D2964F0
for i in range(12):
    for j in range(v_42):
        x = fak()
    print(x)
    v_42 *= 42
```

1, 42, 42^2, 42^3, 42^4, ..., 42^10
