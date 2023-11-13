def sentence_indicator():
    indicator = [".", "?", "!"]
    return indicator


def count(text, indicatorList):
    letterCount = 0
    wordCount = 0
    spaceCount = 0
    sentenceCount = 0
    length = len(text)
    for i in range(length):
        if text[i].isalpha():
            letterCount += 1
        if text[i] in indicatorList:
            sentenceCount += 1
        if text[i] == " ":
            spaceCount += 1
    if letterCount > 1:
        wordCount = spaceCount + 1
    return letterCount, wordCount, sentenceCount


def get_grade(letterCount, wordCount, sentenceCount):
    return int(
        (
            0.0588 * letterCount * 100 / wordCount
            - 0.296 * sentenceCount * 100 / wordCount
            - 15.8
        )
        + 0.5
    )


def main():
    text = input("Text: ")
    letterCount, wordCount, sentenceCount = count(text, sentence_indicator())
    grade = get_grade(letterCount, wordCount, sentenceCount)
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")
    # print(f"Letter: {letterCount}")
    # print(f"Word: {wordCount}")
    # print(f"Sentence: {sentenceCount}")


main()
