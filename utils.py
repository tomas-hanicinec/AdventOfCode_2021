def read_strings(filename):
    with open(filename, 'r') as file:
        return [line.strip('\n') for line in file]


def read_integers(filename):
    with open(filename, 'r') as file:
        return [int(line) for line in file]
