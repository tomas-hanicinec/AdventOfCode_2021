def readIntegers(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            result.append(int(line))
    return result
