def readStrings(filename):
    with open(filename, 'r') as file:
        return [line.strip('\n') for line in file]


def readIntegers(filename):
    with open(filename, 'r') as file:
        return [int(line) for line in file]
