#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>

void pwncollege(char *path, char *const argv[], char *const envp[]) {
    execve(path, argv, envp);
}

int main() {
    char chall[] = "/challenge/embryoio_level34";
    char out[] = "/tmp/gjcjzy";
    int fd = open(out, O_CREAT | O_WRONLY, S_IWUSR | S_IRUSR);
    pid_t fork_pid;

    if ((fork_pid = fork()) == 0) {
        char *args[] = {NULL};
        char *envs[] = {NULL};
        dup2(fd, STDOUT_FILENO);
        pwncollege(chall, args, envs);
    }
    else if (fork_pid == -1) {
        perror("fork() error");
        return 1;
    }
    else {
        wait(NULL);
    }
    close(fd);
    char *args[] = {"/bin/cat", out, NULL};
    char *envs[] = {NULL};
    pwncollege("/bin/cat", args, envs);
    return 0;
}
