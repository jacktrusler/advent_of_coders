#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <omp.h>
#include <xmmintrin.h>

#define ROWS 1000
#define BUFFER_SIZE 16384
#define RUNS 1000

void radix_sort(int arr[], int n)
{
    int max = arr[0];

#pragma omp parallel for reduction(max : max)
    for (int i = 1; i < n; i++)
    {
        _mm_prefetch(&arr[i + 16], _MM_HINT_T0);
        if (arr[i] > max)
            max = arr[i];
    }

    int *output = malloc(n * sizeof(int));

    for (int exp = 1; max / exp > 0; exp *= 10)
    {
        int count[10] = {0};

        {
            int local_count[10] = {0};
            for (int i = 0; i < n; i++)
            {
                _mm_prefetch(&arr[i + 16], _MM_HINT_T0);
                local_count[(arr[i] / exp) % 10]++;
            }

            for (int i = 0; i < 10; i++)
            {
                count[i] += local_count[i];
            }
        }

        for (int i = 1; i < 10; i++)
        {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--)
        {
            _mm_prefetch(&arr[i - 16], _MM_HINT_T0);
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }

        for (int i = 0; i < n; i++)
        {
            _mm_prefetch(&output[i + 16], _MM_HINT_T0);
            arr[i] = output[i];
        }
    }

    free(output);
}

int compare(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

int fast_atoi(const char *str)
{
    return (str[0] - '0') * 10000 +
           (str[1] - '0') * 1000 +
           (str[2] - '0') * 100 +
           (str[3] - '0') * 10 +
           (str[4] - '0');
}

int main(int argc, char *argv[])
{
    clock_t start = clock();

    for (int run = 0; run < RUNS; run++)
    {

        FILE *file = fopen("input.txt", "rb");
        if (file == NULL)
        {
            fprintf(stderr, "ERROR: failed to open file");
            return 1;
        }

        int a[ROWS];
        int b[ROWS];

        char buffer[BUFFER_SIZE];
        setvbuf(file, buffer, _IOFBF, BUFFER_SIZE);
        char line[14];

        for (int i = 0; i < ROWS; i++)
        {
            if (fread(line, 1, 14, file) == 14)
            {
                a[i] = fast_atoi(line);
                b[i] = fast_atoi(line + 8);
            }
        }

        radix_sort(a, ROWS);
        radix_sort(b, ROWS);

        int distance = 0;
        int similarity = 0;
        int table[100000] = {0};

        for (int i = 0; i < ROWS; i++)
        {
            distance += abs(a[i] - b[i]);
            table[a[i]] = a[i];
        }

        for (int j = 0; j < ROWS; j++)
        {
            similarity += table[b[j]];
        }

        printf("%d %d \n", distance, similarity);

        fclose(file);
    }

    clock_t end = clock();
    double duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Completed %d runs\n", RUNS);
    printf("Time taken: %f seconds\n", duration);
    return 0;
}