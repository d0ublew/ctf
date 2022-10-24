#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <string.h>

void pwncollege(char *file, char *unk) {
    execlp(file, file, unk);
}

int main(int argc, char *argv[], char *envp[]) {
    char *path = "/tmp/crlnjt";
    int fd = open(path, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
    if (fd == -1) {
        fprintf(stderr, "Unable to write to %s\n", path);
        close(fd);
        return 1;
    }

    char *password = "yqnuusxx";
    write(fd, password, strlen(password));
    lseek(fd, (off_t) 0, SEEK_SET);

    pid_t fork_pid;
    fork_pid = fork();

    if (fork_pid < 0) {
        perror("fork() error");
        return 1;
    }
    else if (fork_pid == 0) {
        dup2(fd, STDIN_FILENO);
        pwncollege("/challenge/embryoio_level33", (char *) 0);
    }
    else {
        wait(NULL);
    }
    return 0;
}
