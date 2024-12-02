#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define MAX_LEVELS 16
#define MAX_LINE_LENGTH 32
#define RUNS 1000

bool validDifference(int a, int b)
{
    int diff = abs(a - b);
    return diff >= 1 && diff <= 3;
}

bool isValidIncreasing(int *levels, int count)
{
    for (int i = 1; i < count; i++)
    {
        if (levels[i] <= levels[i - 1] || !validDifference(levels[i], levels[i - 1]))
        {
            return false;
        }
    }
    return true;
}

bool isValidDecreasing(int *levels, int count)
{
    for (int i = 1; i < count; i++)
    {
        if (levels[i] >= levels[i - 1] || !validDifference(levels[i], levels[i - 1]))
        {
            return false;
        }
    }
    return true;
}

bool isValidSequence(int *levels, int count)
{
    return isValidIncreasing(levels, count) || isValidDecreasing(levels, count);
}

bool canBeSafeWithRemoval(int *levels, int count)
{
    int temp[MAX_LEVELS];

    for (int skip = 0; skip < count; skip++)
    {
        int idx = 0;
        for (int i = 0; i < count; i++)
        {
            if (i != skip)
            {
                temp[idx++] = levels[i];
            }
        }

        if (isValidSequence(temp, count - 1))
        {
            return true;
        }
    }
    return false;
}

int main()
{
    clock_t start = clock();

    for (int run = 0; run < RUNS; run++)
    {

        char line[MAX_LINE_LENGTH];
        int levels[MAX_LEVELS];
        int safeCount = 0;
        int safeWithDampenerCount = 0;
        int lineCount = 0;

        FILE *file = fopen("input.txt", "rb");
        if (file == NULL)
        {
            fprintf(stderr, "ERROR: failed to open file");
            return 1;
        }

        while (fgets(line, sizeof(line), file))
        {
            int count = 0;
            char *token = strtok(line, " \n");
            while (token != NULL)
            {
                if (count >= MAX_LEVELS)
                {
                    fprintf(stderr, "Warning: Line %d exceeded maximum levels (%d)\n",
                            lineCount + 1, MAX_LEVELS);
                    break;
                }
                levels[count++] = atoi(token);
                token = strtok(NULL, " \n");
            }
            lineCount++;

            bool isSafe = isValidSequence(levels, count);
            if (isSafe)
            {
                safeCount++;
                safeWithDampenerCount++;
            }
            else if (canBeSafeWithRemoval(levels, count))
            {
                safeWithDampenerCount++;
            }
        }

        printf("%d, %d\n", safeCount, safeWithDampenerCount);
        fclose(file);
    }

    clock_t end = clock();
    double duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Completed %d runs\n", RUNS);
    printf("Time taken: %f seconds\n", duration);

    return 0;
}