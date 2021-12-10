from itertools import groupby
from typing import List, Dict, Tuple, Callable

import utils


def main() -> None:
    input_line = utils.read_strings('inputs/day_07.txt')[0]
    positions = [int(n) for n in input_line.split(',')]

    position, fuel_consumption = get_best_position(positions, linear_burn)
    print(f'Best position with linear burn: {position}, fuel spent: {fuel_consumption}')

    position, fuel_consumption = get_best_position(positions, increased_burn)
    print(f'Best position with distance-increased burn: {position}, fuel spent: {fuel_consumption}')


def get_best_position(positions: List[int], fuel_consumption_function: Callable[[int], int]) -> Tuple[int, int]:
    # preprocess data
    max_position = max(positions)
    best_position = -1
    best_fuel = fuel_consumption_function(max_position) * len(positions)  # can't be possibly bigger than this
    counts: Dict[int, int] = {}
    for i, items in groupby(sorted(positions)):
        counts[i] = sum(1 for _ in items)

    # try each possible position
    cache: Dict[int, int] = {}
    for i in range(max_position + 1):
        fuel = 0
        for j in counts:
            distance = i - j if i > j else j - i  # faster than built-in abs()
            if distance not in cache:
                cache[distance] = fuel_consumption_function(distance)
            fuel += (cache[distance] * counts[j])
            if fuel > best_fuel:
                break  # cannot be the best anymore, no need to continue

        if fuel < best_fuel:
            best_position = i
            best_fuel = fuel

    return best_position, int(best_fuel)


def linear_burn(distance: int) -> int:
    return distance


def increased_burn(distance: int) -> int:
    return int((distance * (distance + 1)) / 2)


if __name__ == '__main__':
    main()
