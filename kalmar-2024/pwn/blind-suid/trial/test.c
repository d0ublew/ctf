#include <stdio.h>
#include <string.h>
#include <unistd.h>

char password[] = "poggers";

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    printf("Password: ");
    char buf[32];
    read(0, buf, sizeof(buf));
    int eq = strcmp(buf, password);
    if (!eq) {
        puts("Wrong password");
    }
    return 0;
}
