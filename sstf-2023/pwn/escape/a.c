#include <stdio.h>

int main(void) {
    int val;
    printf("blah%p%nblah", &val, &val);
    printf("val=%d\n", val);
    printf("blah%p%nblah", &val, &val);
    printf("val=%d\n", val);
}
