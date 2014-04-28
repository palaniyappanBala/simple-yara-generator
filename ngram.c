#include <stdio.h>
#include <stdlib.h>


int main(int argc, char* argv[]){
	if(argc < 2){
		return -1;
	}
	long bufsize = 0;
	char *source = NULL;
	FILE *fp = fopen(argv[1], "r");
	if (fp != NULL) {
		/* Go to the end of the file. */
		if (fseek(fp, 0L, SEEK_END) == 0) {
			/* Get the size of the file. */
			bufsize = ftell(fp);
			if (bufsize == -1) { /* Error */ }

			/* Allocate our buffer to that size. */
			source = malloc(sizeof(char) * (bufsize + 1));

			/* Go back to the start of the file. */
			if (fseek(fp, 0L, SEEK_SET) != 0) { /* Error */ }

			/* Read the entire file into memory. */
			size_t newLen = fread(source, sizeof(char), bufsize, fp);
			if (newLen == 0) {
				fputs("Error reading file", stderr);
			} else {
				source[++newLen] = '\0'; /* Just to be safe. */
			}
		}
		fclose(fp);
	}
	
	int ngramsize = 15;
	int i;
	for(i=0; i<bufsize-ngramsize; i++){
		int j;
		for(j=0; j<ngramsize; j++){
			printf("%02x ", source[i+j]&0xff);
		}
		printf("\n");
		
	}
	
	return 0;
}
