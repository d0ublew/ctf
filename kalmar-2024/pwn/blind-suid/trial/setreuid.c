#include <unistd.h>
int main(void) {
    setreuid(0, 0);
    return 0;
}
