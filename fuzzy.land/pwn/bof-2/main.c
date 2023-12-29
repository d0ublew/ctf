#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char flag_path[] = "flag.txt";
const char readonly_mode[] = "r";

void head(char* path, size_t size)
{
  char* flag = NULL;
  FILE* flagfile = fopen(path, readonly_mode);
  if (flagfile == NULL) {
    err(-1, "Sorry couldn't open flag :( report this to the admin!");
  }
  flag = malloc(size);
  if (flag == NULL) {
    err(-1, "malloc failed... this really shouldn't happen");
  }
  memset(flag, 0, size);

  fread(flag, 1, size, flagfile);

  printf("There you go:\n %s\n", flag);

  free(flag);
}

int vuln(void)
{
  char buffer[64];
  fgets(buffer, 0x64, stdin);
}

int main(int argc, char** argv)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  vuln();
  return 0;
}
