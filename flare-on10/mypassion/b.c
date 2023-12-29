#include <stdio.h>

int main(void) {
    char a, b;
    for (a = 32; a < 127; a++) {
        b = 0x127 - a * 4;
        if (b >= 32 && b < 127)
            printf("0%c%c  R@brUc3E\n", a, (char)0x127 - a * 4);
    }
    return 0;
}
