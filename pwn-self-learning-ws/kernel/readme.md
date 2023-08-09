# Note

## QEMU

QEMU shortcut help: `<C-a>h`

Exit QEMU: `<C-a>x`

```console
[    0.734915] Kernel panic - not syncing: Out of memory and no killable processes...
[    0.734915]
[    0.735174] Rebooting in 1 seconds..
```

Increase memory on `qemu`'s `-m` option

## Get Module Load Address

```sh
lsmod | grep '<name>'
cat /proc/modules | grep '<name>'
cat /sys/module/<name>/sections/.text
```

## GDB

### Add Module Symbol

```sh
(gdb) add-symbol-file </path/to/module.ko> <.text address>
```
