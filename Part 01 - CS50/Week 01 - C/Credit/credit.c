#include "cs50.h"
#include <stdio.h>

int cardLength;
int cardParity;
int cardChecksum;
int checksumAdd;
long moduloFactor = 1;
int main(void)
{
    // Prompt for credit card input
    const long cardNumber = get_long("Enter your credit card number: ");
    // Calculate checksum
    while (cardNumber > moduloFactor)
    {
        // Modulo 10
        cardLength++;
        cardParity = cardLength % 2;
        checksumAdd = (cardNumber / moduloFactor) % 10;
        if (cardParity == 1)
        {
            cardChecksum = checksumAdd + cardChecksum;
        }
        else if (cardParity == 0 && checksumAdd < 5)
        {
            cardChecksum = 2 * checksumAdd + cardChecksum;
        }
        else if (cardParity == 0 && checksumAdd >= 5)
        {
            cardChecksum = 2 * checksumAdd % 10 + 2 * checksumAdd / 10 % 10 + cardChecksum;
        }
        moduloFactor *= 10;
        printf("%i\n", cardChecksum);
    }

    printf("%i\n", cardLength);
    int cardPrefix1 = (cardNumber * 10) / moduloFactor;
    int cardPrefix2 = (cardNumber * 100) / moduloFactor;
    if (cardChecksum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else if ((cardPrefix2 == 34 && cardLength == 15) || (cardPrefix2 == 37 && cardLength == 15))
    {
        printf("AMEX\n");
    }
    else if ((cardPrefix2 == 51 && cardLength == 16) || (cardPrefix2 == 52 && cardLength == 16) ||
             (cardPrefix2 == 53 && cardLength == 16) || (cardPrefix2 == 54 && cardLength == 16) ||
             (cardPrefix2 == 55 && cardLength == 16))
    {
        printf("MASTERCARD\n");
    }
    else if ((cardPrefix1 == 4 && cardLength == 13) || (cardPrefix1 == 4 && cardLength == 16))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
