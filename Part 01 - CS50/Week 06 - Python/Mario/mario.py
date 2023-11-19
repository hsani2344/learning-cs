def get_int(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number > 0 and number < 9:
                return number
        except ValueError:
            pass


def mario(number):
    for i in range(number, 0, -1):
        spaceCount = i - 1
        blockCount = number - i + 1
        modified_print(" " * spaceCount)
        modified_print("#" * blockCount)
        modified_print("  ")
        modified_print("#" * blockCount)
        print()


def modified_print(text):
    print(text, end="")


def main():
    height = get_int("Heigh: ")
    mario(height)


main()
