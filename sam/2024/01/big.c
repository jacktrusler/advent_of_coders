#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdbool.h>

#define ROWS 4000000
#define BUFFER_SIZE 32768
#define RUNS 1

int compare(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

int fast_atoi(const char *str)
{
    return (str[0] - '0') * 10000000 +
           (str[1] - '0') * 1000000 +
           (str[2] - '0') * 100000 +
           (str[3] - '0') * 10000 +
           (str[4] - '0') * 1000 +
           (str[5] - '0') * 100 +
           (str[6] - '0') * 10 +
           (str[7] - '0');
}

int main(int argc, char *argv[])
{
    clock_t start = clock();

    for (int run = 0; run < RUNS; run++)
    {

        FILE *file = fopen("bigboy.txt", "rb");
        if (file == NULL)
        {
            fprintf(stderr, "ERROR: failed to open file");
            return 1;
        }

        int *a = malloc(ROWS * sizeof(int));
        int *b = malloc(ROWS * sizeof(int));
        int *table = calloc(100000000, sizeof(int)); // Initialize to 0
        int table[10000000] = {0};

        char buffer[BUFFER_SIZE];
        setvbuf(file, buffer, _IOFBF, BUFFER_SIZE);
        char line[20];

        for (int i = 0; i < ROWS; i++)
        {
            if (fread(line, 1, 20, file) == 20)
            {
                a[i] = fast_atoi(line);
                b[i] = fast_atoi(line + 11);
            }
        }

        qsort(a, ROWS, sizeof(int), compare);
        qsort(b, ROWS, sizeof(int), compare);

        long long distance = 0;
        long long similarity = 0;

        for (int i = 0; i < ROWS; i++)
        {
            distance += (long long)abs(a[i] - b[i]);
            table[a[i]] = a[i];
        }

        for (int j = 0; j < ROWS; j++)
        {
            similarity += (long long)table[b[j]];
        }

        printf("%lld %lld \n", distance, similarity);

        free(a);
        free(b);
        free(table);
        fclose(file);
    }

    clock_t end = clock();
    double duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Completed %d runs\n", RUNS);
    printf("Time taken: %f seconds\n", duration);
    return 0;
}