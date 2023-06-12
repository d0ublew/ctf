#include <stdint.h>
#include <stdio.h>

int g = 0x3D2964F0;
int xor_value = 0x80200003;

unsigned char keys[] = {0x01, 0x19, 0xEF, 0x5A, 0xFA, 0xC8,
                        0x2E, 0x69, 0x31, 0xD7, 0x81, 0x21};

char fak() {
    char lsb = g & 1;
    g = (unsigned int)g >> 1;
    if (lsb)
        g = g ^ xor_value;
    return g & 0xff;
}

uint64_t power(uint64_t b, int e) {
    uint64_t result = b;
    for (int i = 1; i < e; i++) {
        result *= b;
    }
    return result;
}

int main(void) {
    // uint64_t n = 1;
    uint64_t v = 1;
    uint64_t abc[12] = {1};
    for (size_t i = 1; i < 12; i++) {
        v *= 42;
        abc[i] = (v + abc[i - 1] - 1) % UINT32_MAX;
    }
    for (uint32_t i = 1, j = 0; i < UINT32_MAX && j < 12; i++) {
        char x = fak();
        if (i == abc[j] % UINT32_MAX) {
            keys[j] ^= x;
            printf("%c", keys[j++]);
        }
        fflush(stdout);
    }
    puts("");
    return 0;
}
