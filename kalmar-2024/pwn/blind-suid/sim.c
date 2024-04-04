#include <stdint.h>
#include <stdio.h>

uint64_t rol(uint64_t x, uint8_t n) {
    __asm__(".intel_syntax noprefix;"
            "mov rax, rdi;"
            "mov rcx, rsi;"
            "rol rax, rcx;"
            ".att_syntax;");
}

int main(int argc, char *argv[]) {
    char    *v6;
    int64_t  v7;
    uint64_t v8, v9;
    v6 = argv[1];
    // v7 = 11 + 26;
    // v7 = v7 * 26 + 18;
    v7 = 1;
    for (int i = 0; i <= 12 && v6[i]; i++) {
        v7 *= 26LL;
        if (v6[i] > '@' && v6[i] <= 'Z') v7 += v6[i] - 65;
        if (v6[i] > '`' && v6[i] <= 'z') v7 += v6[i] - 97;
    }
    v8 = rol(v7 ^ 0xAAAAAAAAAAAAAAAA, 20);
    printf("%s: %#lx\n", v6, v8);
    for (int j = 0; j <= 15; ++j) {
        v9 = (((v8 >> 12) ^ v8) << 25) ^ (v8 >> 12) ^ v8;
        v8 = (v9 >> 27) ^ v9;
    }
    printf("%s: %#lx\n", v6, v8);
    if (v8 == 0x39403F5DA078C2A) {
        puts("Win");
    } else {
        puts("Nope");
    }
    return 0;
}
