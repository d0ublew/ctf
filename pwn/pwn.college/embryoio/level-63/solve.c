#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

void pwncollege() {}

int main() {
    int fd[2];
    if (pipe(fd) == -1) {
        perror("piping error");
        return 1;
    }
    pid_t chall_pid = fork();

    if (chall_pid == 0) {
        pid_t stdout_pid = fork();
        if (stdout_pid == 0) {
            pid_t stdout_pid_2 = fork();
            if (stdout_pid_2 == 0) {
                close(fd[1]);
                dup2(fd[0], STDIN_FILENO);
                char cmd[] = "/usr/bin/rev";
                char *args[] = {cmd, NULL};
                char *envs[] = {NULL};
                execve(cmd, args, envs);
            } else if (stdout_pid_2 == -1) {
                perror("second stdout fork error");
                return 1;
            } else {
                close(fd[1]);
                dup2(fd[0], STDIN_FILENO);
                char cmd[] = "/usr/bin/rev";
                char *args[] = {cmd, NULL};
                char *envs[] = {NULL};
                execve(cmd, args, envs);
            }
        } else if (stdout_pid == -1) {
            perror("stdout fork() error");
            return 1;
        } else {
            close(fd[0]);
            dup2(fd[1], STDOUT_FILENO);
            char chall[] = "/challenge/embryoio_level63";
            char *args[] = {chall, NULL};
            char *envs[] = {NULL};
            execve(chall, args, envs);
        }

    } else if (chall_pid == -1) {
        perror("chall fork() error");
        return 1;
    } else {
        close(fd[0]);
        close(fd[1]);
        waitpid(chall_pid, NULL, 0);
    }
    return 0;
}
