#include <stdio.h>
#include <string.h>
#include <unistd.h>

char password[] = "K33pth15s3Cret";

int main(void) {
    char buf[32];
    printf("Password: ");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\n")] = 0;
    if (strcmp(password, buf) != 0) {
        puts("Wrong password");
        return 1;
    }
    setreuid(0, 0);
    return 0;
}
