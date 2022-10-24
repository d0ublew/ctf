#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

void pwncollege(char *file) {
    execlp(file, file, (char *) 0);
}

int main(int argc, char *argv[], char *envp[]) {
    int fd[2];
    if (pipe(fd) == -1) {
        fprintf(stderr, "Unable to create pipe\n");
        return 1;
    }

    char password[] = "vjkfhovo\n";
    write(fd[1], password, sizeof(password));
    close(fd[1]);

    pid_t fork_pid;
    fork_pid = fork();

    if (fork_pid < 0) {
        perror("fork() error");
        return 1;
    }
    else if (fork_pid == 0) {
        dup2(fd[0], STDIN_FILENO);
        pwncollege("/challenge/embryoio_level30");
    }
    else {
        wait(NULL);
    }
    close(fd[0]);
    close(fd[1]);

    return 0;
}
