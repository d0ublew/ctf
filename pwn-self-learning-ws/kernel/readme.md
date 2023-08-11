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

## Finding ROP Gadget

Use `-u` and try to use the lower address ones.
Higher address gadgets sometimes fail.

```sh
ropr -u ./vmlinux | grep ': pop rdi; ret;' | head
```

## KASLR

Lowest 20 bits are not randomized?

## /proc/kallsyms

`man nm` for symbol type, e.g., T, t, A, r

```console
000000000002d080 A steal_time
000000000002d0c0 A apf_reason
000000000002e000 A __per_cpu_end
ffffffffa7c00000 T startup_64
ffffffffa7c00000 T _stext
ffffffffa7c00000 T _text
ffffffffa7c00030 T secondary_startup_64
ffffffffa7c000e0 t verify_cpu
ffffffffa7c001e0 T start_cpu0
ffffffffa7c001f0 T __startup_64
ffffffffa7c00430 t pvh_start_xen
```
