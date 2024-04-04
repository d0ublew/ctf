#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    size_t libc_base = 0;
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    if (argc != 2) {
        puts("Missing filename!");
        return EXIT_FAILURE;
    }
    char *filename = argv[1];
    int   child = fork();
    if (child) {
        struct user_regs_struct   regs;
        struct user_fpregs_struct fpregs;

        int from_user;
        int status;
        for (;;) {
            wait(&status);
            if (WIFEXITED(status)) break;
            ptrace(PTRACE_GETREGS, child, NULL, &regs);
            ptrace(PTRACE_GETFPREGS, child, NULL, &fpregs);
            if (regs.rip < 0x0000700000000000) {
                from_user = 1;
                // unsigned long insn =
                //     ptrace(PTRACE_PEEKTEXT, child, regs.rip, NULL);
                // printf("%#llx: %#lx\n", regs.rip, insn);
                // printf("rax: %#llx\n", regs.rax);
                // printf("rbx: %#llx\n", regs.rbx);
                // printf("rcx: %#llx\n", regs.rcx);
                // printf("rdx: %#llx\n", regs.rdx);
                // printf("rdi: %#llx\n", regs.rdi);
                // printf("rsi: %#llx\n", regs.rsi);
                // printf("rsp: %#llx\n", regs.rsp);
                // printf("rbp: %#llx\n", regs.rbp);
                // printf("r8: %#llx\n", regs.r8);
                // printf("r9: %#llx\n", regs.r9);
                // printf("r10: %#llx\n", regs.r10);
                // printf("r11: %#llx\n", regs.r11);
                // printf("r12: %#llx\n", regs.r12);
                // printf("r13: %#llx\n", regs.r13);
                // printf("r14: %#llx\n", regs.r14);
                // printf("r15: %#llx\n", regs.r15);
                // printf("rip: %#llx\n", regs.rip);
            } else if (from_user) {
                if (!libc_base && (regs.rip & 0xfff) == 0xdc0) {
                    libc_base = regs.rip - 0x29dc0;
                    printf("libc_base: %#zx\n", libc_base);
                }
                printf("rip: %#llx\n", regs.rip);
                // printf("rax: %#llx\n", regs.rax);
                // printf("rbx: %#llx\n", regs.rbx);
                // printf("rcx: %#llx\n", regs.rcx);
                // printf("rdx: %#llx\n", regs.rdx);
                // printf("rdi: %#llx\n", regs.rdi);
                // printf("rsi: %#llx\n", regs.rsi);
                // printf("rsp: %#llx\n", regs.rsp);
                // printf("rbp: %#llx\n", regs.rbp);
                // printf("r8: %#llx\n", regs.r8);
                // printf("r9: %#llx\n", regs.r9);
                // printf("r10: %#llx\n", regs.r10);
                // printf("r11: %#llx\n", regs.r11);
                // printf("r12: %#llx\n", regs.r12);
                // printf("r13: %#llx\n", regs.r13);
                // printf("r14: %#llx\n", regs.r14);
                // printf("r15: %#llx\n", regs.r15);
                // puts("---");
                from_user = 0;
            }
            // if (regs.rip > libc_base + 0x198940 &&
            //     regs.rip < libc_base + 0x198d80) {
            //     printf("rip: %#llx\n", regs.rip);
            //     if (regs.rip == libc_base + 0x198962) {
            //         for (size_t i = 0; i < 256; i++) {
            //             char *ptr = (char *)&fpregs.xmm_space[0];
            //             printf("%c", *(ptr + i));
            //         }
            //         puts("");
            //     }
            //     for (size_t i = 0; i < 16; i++) {
            //         printf("xmm%02zu: %08x%08x%08x%08x\n", i,
            //                fpregs.xmm_space[i * 4 + 3],
            //                fpregs.xmm_space[i * 4 + 2],
            //                fpregs.xmm_space[i * 4 + 1],
            //                fpregs.xmm_space[i * 4 + 0]);
            //     }
            //     puts("");
            // }
            // if (regs.rip == libc_base + 0x198962) {
            //     puts("--start--");
            //     puts("\n--end--");
            // }
            ptrace(PTRACE_SINGLESTEP, child, NULL, NULL);
        }
    } else {
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execl(filename, filename, NULL);
    }
    return EXIT_SUCCESS;
}
