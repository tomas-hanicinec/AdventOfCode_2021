from typing import List

import utils


class Day01:
    depths: List[int]

    def __init__(self) -> None:
        self.depths = utils.read_integers('inputs/day_01.txt')

    def run(self) -> str:
        return (
            f'{self.count_increases(1)} measurements are larger than the previous measurement\n'
            f'{self.count_increases(3)} sums that are larger than the previous sum'
        )

    def count_increases(self, window_size: int) -> int:
        previous_sum = sum(self.depths[0:window_size])

        # loop through the rest of the input, count increases
        result = 0
        for i, depth in enumerate(self.depths[window_size:]):
            current_sum = previous_sum + depth - self.depths[i]  # slide the window forward
            if current_sum > previous_sum:
                result += 1

            previous_sum = current_sum

        return result


if __name__ == '__main__':
    print(Day01().run())
