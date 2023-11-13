# Prompt user for credit card
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


# Calculate checksum
def calculate(number):
    checksum = 0
    length = 0
    while number > 0:
        checksum += number % 10
        number = int(number / 10)
        length += 1
        if number > 0:
            tmp = 2 * (number % 10)
            number = int(number / 10)
            length += 1
            while tmp > 0:
                checksum += tmp % 10
                tmp = int(tmp / 10)
    return checksum, length


# Validate the card and print
# AMEX, VISA or MASTERCARD
def validate(number, checksum, length):
    d = {
        34: {"length": [15], "name": "AMEX"},
        37: {"length": [15], "name": "AMEX"},
        51: {"length": [16], "name": "MASTERCARD"},
        52: {"length": [16], "name": "MASTERCARD"},
        53: {"length": [16], "name": "MASTERCARD"},
        54: {"length": [16], "name": "MASTERCARD"},
        55: {"length": [16], "name": "MASTERCARD"},
        4: {"length": [13, 16], "name": "VISA"},
    }
    # Trim the credit card to get the prefix
    prefix_digits = 2
    prefix = number
    for i in range(length - prefix_digits):
        prefix = int(prefix / 10)
    if checksum % 10 != 0:
        print("INVALID")
    else:
        # Multiple prefix are tried
        for i in range(1, prefix_digits + 1, 1):
            try:
                if length in d[prefix]["length"]:
                    print(d[prefix]["name"])
                    return
            except KeyError:
                pass
            # Remove the last digit of the prefix
            prefix = int(prefix / 10)
        # None of the prefix tried was found in the dictionary
        print("INVALID")


def main():
    creditCard = get_int("Number: ")
    checksum, length = calculate(creditCard)
    validate(creditCard, checksum, length)


main()
