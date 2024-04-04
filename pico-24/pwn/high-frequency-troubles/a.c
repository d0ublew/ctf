#include <stdio.h>
#include <stdlib.h>
int main(void) {
  printf("%lx\n", 4 * 1024 * 1024 * sizeof(long));
  return EXIT_SUCCESS;
}
