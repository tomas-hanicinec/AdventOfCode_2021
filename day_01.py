from typing import List

import utils


def main() -> None:
    depths = utils.read_integers('inputs/day_01.txt')
    print(f'{count_increases(depths, 1)} measurements are larger than the previous measurement')
    print(f'{count_increases(depths, 3)} sums that are larger than the previous sum')


def count_increases(depths: List[int], window_size: int) -> int:
    # calculate the first window sum
    previous_sum: int = 0
    for depth in depths[0:window_size]:
        previous_sum += depth

    # loop through the rest of the input, count increases
    result: int = 0
    index = window_size
    while index < len(depths):
        current_sum = previous_sum + depths[index] - depths[index - window_size]  # slide the window forward
        if current_sum > previous_sum:
            result += 1

        previous_sum = current_sum
        index += 1

    return result


if __name__ == '__main__':
    main()
