#include <stdio.h>
#include <unistd.h>

void pwncollege(char *path, char *const *argv, char *const *envp) {
    execve(path, argv, envp);
}

int main(int argc, char *argv[], char *envp[]) {
    char chall[] = "/challenge/embryoio_level29";
    pid_t fork_pid;

    fork_pid = fork();
    if (fork_pid < 0) {
        return 1;
    }
    else if (fork_pid == 0) {
        char *args[] = {chall, NULL};
        pwncollege("/challenge/embryoio_level29", args, NULL);
    }
    else {
        wait(NULL);
    }
    return 0;
}
