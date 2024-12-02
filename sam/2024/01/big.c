#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <omp.h>
#include <xmmintrin.h>
#include <windows.h>

#define ROWS 4000000
#define BUFFER_SIZE 65536

void parallel_radix_sort(int *arr, int n)
{
    if (n <= 1)
        return;

    int max_threads = omp_get_max_threads();
    int **local_counts = malloc(max_threads * sizeof(int *));
    for (int i = 0; i < max_threads; i++)
    {
        local_counts[i] = calloc(256, sizeof(int));
    }

    int *output = malloc(n * sizeof(int));

    for (int shift = 0; shift < 32; shift += 8)
    {
#pragma omp parallel for schedule(static)
        for (int t = 0; t < max_threads; t++)
        {
            memset(local_counts[t], 0, 256 * sizeof(int));
        }

#pragma omp parallel
        {
            int tid = omp_get_thread_num();
            int *my_counts = local_counts[tid];

#pragma omp for schedule(static)
            for (int i = 0; i < n; i++)
            {
                unsigned byte = (unsigned)(arr[i] >> shift) & 0xFF;
                my_counts[byte]++;
            }
        }

        int total = 0;
        for (int byte = 0; byte < 256; byte++)
        {
            int sum = 0;
            for (int t = 0; t < max_threads; t++)
            {
                int temp = local_counts[t][byte];
                local_counts[t][byte] = total + sum;
                sum += temp;
            }
            total += sum;
        }

#pragma omp parallel
        {
            int tid = omp_get_thread_num();
            int *my_counts = local_counts[tid];

#pragma omp for schedule(static)
            for (int i = 0; i < n; i++)
            {
                unsigned byte = (unsigned)(arr[i] >> shift) & 0xFF;
                output[my_counts[byte]++] = arr[i];
            }
        }

#pragma omp parallel for schedule(static)
        for (int i = 0; i < n; i++)
        {
            arr[i] = output[i];
        }
    }

    free(output);
    for (int i = 0; i < max_threads; i++)
    {
        free(local_counts[i]);
    }
    free(local_counts);
}

int binary_search(int arr[], int size, int target)
{
    int left = 0;
    int right = size - 1;
    int result = -1; // Return -1 if not found

    while (left <= right)
    {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target)
        {
            result = mid;    // Found it, but might not be first
            right = mid - 1; // Keep searching left
        }
        else if (arr[mid] < target)
        {
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }

    return result;
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

    HANDLE hFile = CreateFile("bigboy.txt", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        fprintf(stderr, "CreateFile failed\n");
        return 1;
    }

    HANDLE hMapping = CreateFileMapping(hFile, NULL, PAGE_READONLY, 0, 0, NULL);
    if (hMapping == NULL)
    {
        CloseHandle(hFile);
        fprintf(stderr, "CreateFileMapping failed\n");
        return 1;
    }

    char *file_content = (char *)MapViewOfFile(hMapping, FILE_MAP_READ, 0, 0, 0);
    if (file_content == NULL)
    {
        CloseHandle(hMapping);
        CloseHandle(hFile);
        fprintf(stderr, "MapViewOfFile failed\n");
        return 1;
    }

    int *a = malloc(ROWS * 2 * sizeof(int));
    int *b = a + ROWS;

#pragma omp parallel for
    for (int i = 0; i < ROWS; i++)
    {
        char *line = file_content + (i * 20);
        a[i] = fast_atoi(line);
        b[i] = fast_atoi(line + 11);
    }

    parallel_radix_sort(a, ROWS);
    parallel_radix_sort(b, ROWS);

    long long distance = 0;
    long long similarity = 0;
#pragma omp parallel for reduction(+ : distance, similarity)
    for (int i = 0; i < ROWS; i++)
    {
        _mm_prefetch(&a[i + 16], _MM_HINT_T0);
        _mm_prefetch(&b[i + 16], _MM_HINT_T0);
        int ai = a[i];
        distance += abs(ai - b[i]);
        int pos = binary_search(b, ROWS, ai);
        if (pos >= 0)
        {
            int count = 0;
            while (b[pos + count] == ai)
            {
                count++;
            }
            similarity += ai * count;
        }
    }

    printf("%lld %lld \n", distance, similarity);

    CloseHandle(hMapping);
    CloseHandle(hFile);
    UnmapViewOfFile(file_content);
    free(a);

    clock_t end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", duration);
    return 0;
}