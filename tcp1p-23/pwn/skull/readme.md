# Solution

`ioctl(fd, 0x6969, ...)` has arbitrary read primitive since the first
`copy_from_user` reads in 16 byte which then populates `local_18`. The next
`copy_to_user` would copy whatever `local_18` is pointing to, to us

```c
  if (param_2 == 0x6969) {
    lVar1 = _copy_from_user(&local_20,param_3,0x10);
    if (lVar1 == 0) {
      lVar1 = _copy_to_user(param_3,local_18,8);
      if (lVar1 != 0) {
        FUN_0010017f();
        return;
      }
    }
    else {
      _printk(&DAT_0010020e);
    }
  }
```

`ioctl(fd, 0xfade, ...)` has arbitrary write primitive. The second `copy_from_user`
uses `local_20` instead of `&local_20`, enables us to write into whatever
`local_20` is pointing to (`local_18` is controlled by us)

```c
  else if (param_2 == 0xfade) {
    lVar1 = _copy_from_user(&local_20,param_3,0x10);
    if (lVar1 == 0) {
      lVar1 = _copy_from_user(local_20,local_18,8);
      if (lVar1 != 0) {
        FUN_0010014f();
        return;
      }
    }
    else {
      _printk(&DAT_00100246);
    }
  }
```

defeat `KASLR` by leaking unradomized kernel address near `cpu_entry_area` (<https://ret2school.github.io/post/iwindow/>)

overwrite `modprobe_path` to do privesc
