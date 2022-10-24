#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>

void pwncollege(char *path, char *const argv[], char *const envp[]) {
    execve(path, argv, envp);
}

int main() {
    char chall[] = "/challenge/embryoio_level35";
    pid_t fork_pid;

    if ((fork_pid = fork()) == 0) {
        char *args[] = {NULL};
        char *envs[] = {NULL};
        pwncollege(chall, args, envs);
    }
    else if (fork_pid == -1) {
        perror("fork() error");
        return 1;
    }
    else {
        wait(NULL);
    }
    return 0;
}
