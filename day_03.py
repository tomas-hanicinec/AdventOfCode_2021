from typing import Callable, List

import utils


class Day03:
    binary_strings: List[str]
    bit_count: int

    def __init__(self) -> None:
        self.binary_strings = utils.read_strings('inputs/day_03.txt')
        self.bit_count = len(self.binary_strings[0])

    def run(self) -> str:
        gamma_rate = epsilon_rate = 0
        for i in range(self.bit_count):
            most_common = get_most_common_bit(self.binary_strings, i)
            gamma_rate = (gamma_rate << 1) + most_common
            epsilon_rate = (epsilon_rate << 1) + 1 - most_common

        o2_generator_rating = self._reduce_by_criteria(
            lambda index, most_common_bit: lambda number_string: int(number_string[index]) == most_common_bit
        )
        co2_scrubber_rating = self._reduce_by_criteria(
            lambda index, most_common_bit: lambda number_string: int(number_string[index]) != most_common_bit
        )

        return (
            f'Submarine power consumption: {gamma_rate * epsilon_rate}\n'
            f'Submarine life support rating: {int(o2_generator_rating, 2) * int(co2_scrubber_rating, 2)}'
        )

    def _reduce_by_criteria(self, filter_factory: Callable[[int, int], Callable[[str], int]]) -> str:
        remaining = self.binary_strings
        for i in range(self.bit_count):
            most_common = get_most_common_bit(remaining, i)
            filter_function = filter_factory(i, most_common)
            remaining = list(filter(filter_function, remaining))
            if len(remaining) == 1:
                return remaining[0]  # filtered down to a single binary string
        else:
            raise Exception('invalid input, could not reduce the binary strings to a single number')


def get_most_common_bit(binary_strings: List[str], position: int) -> int:
    bit_sum = sum([int(n[position]) for n in binary_strings])
    remainder = len(binary_strings) - bit_sum
    return 0 if bit_sum < remainder else 1


if __name__ == '__main__':
    print(Day03().run())
