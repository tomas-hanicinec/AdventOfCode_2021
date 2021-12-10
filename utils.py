from typing import List


def read_strings(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return [line.strip('\n') for line in file]


def read_integers(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        return [int(line) for line in file]
