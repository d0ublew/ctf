#include <algorithm>
#include <limits.h>
#include <stdio.h>

unsigned int x = 0x3D2964F0;

unsigned int fuck() {
    unsigned int v1 = x & 1;
    x >>= 1;
    x ^= -v1 & 0x80200003;
    return x;
}

unsigned char ida_chars[] = {0x01, 0x19, 0xEF, 0x5A, 0xFA, 0xC8,
                             0x2E, 0x69, 0x31, 0xD7, 0x81, 0x21};

int main() {
    setbuf(stdout, NULL);
    int countEven = 0, countOdd = 0;
    unsigned long v = 1;
    std::pair<unsigned long, unsigned int> abc[12];
    abc[0] = {0, 0};
    for (int i = 1; i < 12; ++i) {
        v *= 42lu;
        abc[i] = {(abc[i - 1].first + v) % __UINT32_MAX__, i};
    }

    // for (int i = 0; i < 12; ++i) {
    //     abc[i].first = (abc[i].first - 1) % __UINT32_MAX__;
    // }

    // sort for loop below
    std::sort(abc, abc + 12);

    for (unsigned int i = 0, j = 0; i < __UINT32_MAX__ && j < 12; ++i) {
        fuck();
        if (i == abc[j].first) {
            ida_chars[abc[j++].second] ^= x & 0xff;
        }
    }

    printf("ACSC{");
    for (int i = 0; i < 12; ++i) {
        printf("%c", ida_chars[i]);
    }
    puts("}");
}
