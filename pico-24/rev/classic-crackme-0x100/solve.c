#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  char output[] = "xjagpediegzqlnaudqfwyncpvkqneusycourkguerjpzcbstcc";
  char input[51];
  int random1, random2;
  int secret1 = 85;
  int secret2 = 51;
  int secret3 = 15;
  char fix = 97;
  int len = strlen(output);
  int i_0 = 0;
  for (i_0 = 0; i_0 < len; i_0++) {
    for (unsigned char n = 0x20; n < 0x7f; n++) {
      int i = 0;
      unsigned char x = n;
      while (i <= 2) {
        random1 = (secret1 & (i_0 % 255)) + (secret1 & ((i_0 % 255) >> 1));
        random2 = (random1 & secret2) + (secret2 & (random1 >> 2));
        x = ((random2 & secret3) + x - fix + (secret3 & (random2 >> 4))) % 26 +
            fix;
        ++i;
      }
      if (x == output[i_0]) {
        input[i_0] = n;
        break;
      }
    }
  }
  printf("%s\n", input);

  return EXIT_SUCCESS;
}
