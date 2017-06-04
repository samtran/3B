#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "ext2_fs.h"
#include <unistd.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[]){
  // Check arguments
  if(argc != 2){
   fprintf(stderr, "Invalid argument. Required file...exiting!\n");
    exit(1);
  }

  exit(0); 
}
