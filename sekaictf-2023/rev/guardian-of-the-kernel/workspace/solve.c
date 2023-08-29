#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define LAYER_1 0x7000
#define LAYER_2 0x7001
#define LAYER_3 0x7002
#define DEVICE_NAME "/proc/Flag-Checker"

int global_fd;

void open_dev(void) {
    global_fd = open(DEVICE_NAME, O_RDWR);
    if (global_fd < 0) {
        puts("[!] Failed to open device");
        exit(EXIT_FAILURE);
    }
    puts("[*] Device opened");
}

int main(void) {
    int rc;
    open_dev();
    char part1[] = "SEKAI{";
    rc = ioctl(global_fd, LAYER_1, part1);
    if (!rc) {
        puts("[!] Failed to unlock layer 1");
        exit(EXIT_FAILURE);
    }
    puts("[*] Unlocked layer 1");

    char part2[8];
    for (size_t i = 0; i < 10000000; i++) {
        sprintf(part2, "%07zu", i);
        part2[7] = 0;
        rc = ioctl(global_fd, LAYER_2, part2);
        if (rc) {
            printf("%s\n", part2);
            break;
        }
        if (i == 9999999) {
            puts("[!] Failed to unlock layer 2");
            exit(EXIT_FAILURE);
        }
    }
    puts("[*] Unlocked layer 2");

    char part3[13] = {0x0e, 0xaf, 0x88, 0x1d, 0xb9, 0x88, 0x8c,
                      'x',  0xec, 0x11, 0xf3, '}',  0};
    for (int i = 10; i >= 0; i--) {
        part3[i] -= part3[i + 1] * ~i;
    }
    printf("%s\n", part3);
    rc = ioctl(global_fd, LAYER_3, part3);
    if (!rc) {
        puts("[!] Failed to unlock layer 3");
        exit(EXIT_FAILURE);
    }
    puts("[*] Unlocked layer 3");

    printf("Flag: %s%s%s\n", part1, part2, part3);
    return 0;
}
