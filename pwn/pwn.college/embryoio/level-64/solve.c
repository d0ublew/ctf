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

    pid_t pid_1 = fork();

    if (pid_1 == 0) {
        pid_t pid_2 = fork();
        if (pid_2 == 0) {
            // TODO: third fork
            pid_t pid_3 = fork();
            if (pid_3 == 0) {
                close(fd[0]);
                char password[] = "jjqalfct";
                write(fd[1], password, sizeof(password));
            }
            dup2(df[0], STDIN_FILENO);
            dup2(fd[1], STDOUT_FILENO);
            char cmd[] = "/usr/bin/cat";
            char *args[] = {cmd, "-", NULL};
            char *envs[] = {NULL};
            execve(cmd, args, envs);
        } else if (pid_2 == -1) {
            perror("second fork() error");
            return 1;
        } else {
            dup2(fd[0], STDIN_FILENO);
            char cmd[] = "/challenge/embryoio_level64";
            char *args[] = {cmd, NULL};
            char *envs[] = {NULL};
            execve(cmd, args, envs);
            waitpid(pid_2, NULL, 0);
            close(fd[0]);
        }

    } else if (pid_1 == -1) {
        perror("first fork() error");
        return 1;
    } else {
        close(fd[0]);
        close(fd[1]);
        waitpid(pid_1, NULL, 0);
    }
    return 0;
}
