#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <omp.h>
#include <xmmintrin.h>

#define ROWS 4000000
#define BUFFER_SIZE 65536
#define RUNS 1

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

#pragma omp parallel
        {
            int local_count[10] = {0};
#pragma omp for
            for (int i = 0; i < n; i++)
            {
                _mm_prefetch(&arr[i + 16], _MM_HINT_T0);
                local_count[(arr[i] / exp) % 10]++;
            }

#pragma omp critical
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

#pragma omp parallel for
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
    return (str[0] - '0') * 10000000 +
           (str[1] - '0') * 1000000 +
           (str[2] - '0') * 100000 +
           (str[3] - '0') * 10000 +
           (str[4] - '0') * 1000 +
           (str[5] - '0') * 100 +
           (str[6] - '0') * 10 +
           (str[7] - '0');
}

int main()
{
    clock_t start = clock();
    double duration;

    omp_set_num_threads(16);

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

        radix_sort(a, ROWS);
        radix_sort(b, ROWS);

        long long distance = 0;
#pragma omp parallel for reduction(+ : distance)
        for (int i = 0; i < ROWS; i++)
        {
            _mm_prefetch(&a[i + 16], _MM_HINT_T0);
            _mm_prefetch(&b[i + 16], _MM_HINT_T0);
            distance += abs(a[i] - b[i]);
        }

#pragma omp parallel for
        for (int i = 0; i < ROWS; i++)
        {
#pragma omp atomic write
            table[a[i]] = a[i];
        }

        long long similarity = 0;
#pragma omp parallel for reduction(+ : similarity)
        for (int j = 0; j < ROWS; j++)
        {
            similarity += table[b[j]];
        }

        printf("%lld %lld \n", distance, similarity);

        free(a);
        free(b);
        free(table);
        fclose(file);
    }

    clock_t end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Completed %d runs\n", RUNS);
    printf("Time taken: %f seconds\n", duration);
    return 0;
}