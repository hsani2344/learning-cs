import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Invalid usage")
        return 1
    # TODO: Read database file into a variable
    csvFile = sys.argv[1]
    csvBuffer = open(csvFile, mode="r")
    csvData = csv.DictReader(csvBuffer)
    # DEBUG
    # print(csvData)
    # TODO: Read DNA sequence file into a variable
    sequenceFile = sys.argv[2]
    sequenceBuffer = open(sequenceFile, mode="r")
    sequence = sequenceBuffer.readline()
    # TODO: Find longest match of each STR in DNA sequence
    dictList = list()
    for element in csvData:
        dictList.append(element)
    subsqcList = list(dictList[0])
    subsqcCountDict = dict()
    for subsqc in subsqcList:
        subsqcCountDict[subsqc] = longest_match(sequence, subsqc)
    # print(subsqcCountDict)
    for dictionary in dictList:
        if subsequence_match(dictionary, subsqcCountDict, subsqcList):
            print(dictionary["name"])
            return
    else:
        print("No match")
    # DEBUG
    # print(sequence)
    # print(dictList)
    # print(subsqcList)
    # print(subsqcCountDict)
    # TODO: Check database for matching profiles
    return


def subsequence_match(dictionary, subsqcCountDict, subsqcList):
    sq_count = len(subsqcList)
    for i in range(1, sq_count, 1):
        # print(f"{dictionary[i]} =? {subsqcCountDict[i]} - {i} - {dictionary}")
        try:
            if int(dictionary[subsqcList[i]]) != (subsqcCountDict[subsqcList[i]]):
                return False
        except KeyError:
            pass
    return True


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
