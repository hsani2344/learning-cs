#include "cs50.h"
#include <stdio.h>

int main(void)
{
    // Height is required by the main
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    // Loop require the variable height
    int blockCount = 1;
    const int gapCount = 2;
    int spaceNumber = height - blockCount;
    do
    {
        for (int i = 0; i < spaceNumber; i++)
        {
            printf(" ");
        }
        for (int i = 0; i < blockCount; i++)
        {
            printf("#");
        }

        for (int i = 0; i < gapCount; i++)
        {
            printf(" ");
        }
        for (int i = 0; i < blockCount; i++)
        {
            printf("#");
        }
        printf("\n");
        spaceNumber--;
        blockCount++;
    }
    while (spaceNumber >= 0);
}
