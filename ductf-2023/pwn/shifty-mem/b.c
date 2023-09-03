#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_STR_LEN 128

int main(int argc, char **argv) {
    char out[MAX_STR_LEN] = "HACKEDHACKED\0";

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <name>\n", argv[0]);
        exit(1);
    }

    char *name = argv[1];
    int fd = shm_open(name, O_RDWR, S_IRWXU | S_IRWXG | S_IRWXO);
    if (fd == -1) {
        fprintf(stderr, "shm_open error");
        exit(1);
    }
    getchar();
    write(fd, out, MAX_STR_LEN);
    return 0;
}
