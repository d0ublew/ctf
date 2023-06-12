#include <stdint.h>
#include <stdio.h>

typedef unsigned char uchar_t;

#define START_STATE 0xACE1
uint16_t current_state = START_STATE;
uint16_t mask = 0xB400;

uchar_t galois_lfsr() {
    uchar_t lsb = current_state & 1;
    current_state >>= 1;
    if (lsb)
        current_state ^= mask;
    return current_state & 0xff;
}

int main(void) {
    // It loops around after going through 65535 (UINT16_MAX) times
    printf("%x\n", current_state);
    for (uint16_t i = 0; i < UINT16_MAX; i++) {
        printf("%hu ", i);
        fflush(stdout);
        galois_lfsr();
    }
    puts("");
    // It loops around after going through 65535 (UINT16_MAX) times
    printf("%x\n", current_state);
    for (uint16_t i = 0; i < UINT16_MAX; i++) {
        galois_lfsr();
    }
    // It loops around after going through 65535 (UINT16_MAX) times
    printf("%x\n", current_state);
    return 0;
}
