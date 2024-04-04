#include <fcntl.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/personality.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

#define INFO(msg, ...)                                                         \
    { printf("[*] " msg "\n", ##__VA_ARGS__); }

#define PANIC(msg, ...)                                                        \
    {                                                                          \
        fprintf(stderr, "[!] " msg "\n", ##__VA_ARGS__);                       \
        exit(EXIT_FAILURE);                                                    \
    }

#define DEBUG(msg, ...)                                                        \
    {                                                                          \
        if (DEBUG_FLAG) {                                                      \
            fprintf(stderr, "[D] " msg "\n", ##__VA_ARGS__);                   \
        }                                                                      \
    }

#define ERR(msg)                                                               \
    {                                                                          \
        fprintf(stderr, "[!] (%s:%d) ", __FILE__, __LINE__);                   \
        perror(msg);                                                           \
        exit(EXIT_FAILURE);                                                    \
    }

#define __libc_start_main_off 0x29dc0
#define write_syscall_off     0x114885

size_t libc_base = 0;
size_t pie_base = 0;
char   DEBUG_FLAG = 0;

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <suid binary> <output file descriptor>",
                argv[0]);
        exit(EXIT_FAILURE);
    }
    char *filename = argv[1];
    int   out_fd = atoi(argv[2]);
    if (out_fd > 255 || out_fd < 3) {
        PANIC("Invalid file descriptor: found %d, expected (3-255)", out_fd);
    }

    if (getenv("DEBUG")) {
        DEBUG_FLAG = 1;
    }
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    pid_t child = fork();
    if (child == 0) {
        // child process
        if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
            ERR("ptrace");
        }
        prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
        personality(ADDR_NO_RANDOMIZE); // optional
        execl(filename, filename, NULL);
    } else if (child > 0) {
        int status = 0;
        int from_user = 1;
        int done = 0;
        while (1) {
            waitpid(child, &status, 0);
            if (WIFEXITED(status)) break;
            uint64_t rip = ptrace(PTRACE_PEEKUSER, child,
                                  offsetof(struct user, regs.rip), NULL);
            if (rip < 0x0000700000000000) {
                if (!pie_base && libc_base && (rip & 0xfff) == 0) {
                    pie_base = rip - 0x1000; // rip is pointing to `_init`
                    INFO("pie_base: %#zx", pie_base);
                }
                DEBUG("rip: %#lx", rip);
                from_user = 1;
            } else if (from_user) {
                DEBUG("rip: %#lx", rip);
                if (!libc_base && (rip & 0xfff) == 0xdc0) {
                    libc_base = rip - 0x29dc0; // libc_start_main
                    INFO("libc_base: %#zx", libc_base);
                }
                from_user = 0;
            }
            if (!done && rip == libc_base + write_syscall_off && pie_base) {
                INFO("Dumping binary...");
                ptrace(PTRACE_POKEUSER, child, offsetof(struct user, regs.rdi),
                       69);
                ptrace(PTRACE_POKEUSER, child, offsetof(struct user, regs.rsi),
                       pie_base);
                ptrace(PTRACE_POKEUSER, child, offsetof(struct user, regs.rdx),
                       0x5000);
                done = 1;
            }
            ptrace(PTRACE_SINGLESTEP, child, NULL, NULL);
            if (done) break;
        }
        ptrace(PTRACE_DETACH, child, NULL, NULL);
        INFO("Done");
        execl("/bin/bash", "/bin/bash", NULL);
    } else {
        ERR("fork");
    }

    return EXIT_SUCCESS;
}
