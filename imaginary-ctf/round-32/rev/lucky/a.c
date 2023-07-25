#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    srand(1337);
    uint16_t a, b;
    int byte;
    byte = rand();
    a = (uint16_t)(byte >> 0xf) | 1;
    byte = rand();
    b = (uint16_t)(byte >> 0xf) | 1;
    printf("%hu %hu\n", a, b);
}
