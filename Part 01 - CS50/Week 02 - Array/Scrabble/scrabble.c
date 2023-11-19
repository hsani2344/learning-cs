#include "cs50.h"
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
string word[2];

int compute_score(string something);
int player;
bool alpha;
int score[2];

int main(void)
{
    // Get input words from the TWO players
    for (int i = 0; i < 2; i++)
    {
        player = i;
        // Prompt MUST be alphabetical
        do
        {
            alpha = false;
            // Always add +1 to player for the user
            word[player] = get_string("Player %i: ", player + 1);
            for (int j = 0; word[player][j] != 0; j++)
            {
                if (isalpha(word[player][j]))
                {
                    alpha = true;
                }
            }
        }
        while (alpha == false);
        // Score both words
        score[player] = compute_score(word[player]);
        printf("This is the score: %i\n", score[player]);
    }

    // Print the winner
    for (int i = 0; i < 1; i++)
    {
        if (score[i] == score[i + 1])
        {
            printf("Tie!\n");
        }
        // Always add +1 to player for the user
        // Player 1 wins
        else if (score[i] > score[i + 1])
        {
            printf("Player %i wins!\n", i + 1);
        }
        // Player 2 wins
        else if (score[i] < score[i + 1])
        {
            printf("Player %i wins!\n", i + 2);
        }
    }
}

int x;
int compute_score(string something)
{
    // Compute and return score for string
    x = 0;
    for (int i = 0; something[i] != 0; i++)
    {
        if ((int) toupper(something[i]) > 64 && toupper(something[i]) < 90)
        {
            x += POINTS[(int) toupper(something[i]) - 65];
        }
    }
    return x;
}
