#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define ROWS 1000

int compare(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

int main(int argc, char *argv[])
{
    clock_t start = clock();

    FILE *file = fopen("input.txt", "r");
    if (file == NULL)
    {
        fprintf(stderr, "ERROR: failed to open file");
        return 1;
    }

    int a[ROWS];
    int b[ROWS];

    for (int i = 0; i < ROWS; i++)
    {
        if (fscanf(file, "%d %d", &a[i], &b[i]) != 2)
        {
            printf("Error reading line %d\n", i + 1);
            fclose(file);
            return 1;
        }
    }

    if (strcmp(argv[1], "1") == 0)
    {

        qsort(a, ROWS, sizeof(int), compare);
        qsort(b, ROWS, sizeof(int), compare);

        int distance = 0;
        for (int i = 0; i < ROWS; i++)
        {
            distance += abs(a[i] - b[i]);
        }

        printf("%d \n", distance);
    }
    else
    {
        int similarity = 0;
        int table[100000] = {0};

        for (int i = 0; i < ROWS; i++)
        {
            table[a[i]] = a[i];
        }

        for (int j = 0; j < ROWS; j++)
        {
            similarity += table[b[j]];
        }

        printf("%d \n", similarity);
    }

    fclose(file);

    clock_t end = clock();
    double duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", duration);
    return 0;
}