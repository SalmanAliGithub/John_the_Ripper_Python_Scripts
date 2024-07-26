#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define KEYSIZE 16
#define START_TIME 1524020929

void main() {
	int i;
	char key[KEYSIZE];
	long long j;
	FILE *file;
	
	file = fopen("generated_keys.txt", "w");
	if (file == NULL) {
		printf("Error opening file!\n");
		exit(1);	
	}

	for (j = START_TIME - 60 * 60 * 2; j < START_TIME; j++) {
		srand(j);
		for (i = 0; i < KEYSIZE; i++) {
			key[i] = rand() % 256;
			fprintf(file, "%.2x", (unsigned char)key[i]);		
		}	
		fprintf(file, "\n");
	}
	fclose(file);
}