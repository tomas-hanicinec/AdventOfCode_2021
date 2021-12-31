from itertools import groupby
from typing import Dict, Tuple, Callable, List

import utils


class Day07:
    positions: List[int]

    def __init__(self) -> None:
        input_line = utils.read_strings('inputs/day_07.txt')[0]
        self.positions = [int(n) for n in input_line.split(',')]

    def run(self) -> str:
        def linear_burn(distance: int) -> int:
            return distance

        def increased_burn(distance: int) -> int:
            return (distance * (distance + 1)) // 2

        result = ''
        position, fuel_consumption = self.get_best_position(linear_burn)
        result += f'Best position with linear burn: {position}, fuel spent: {fuel_consumption}\n'

        position, fuel_consumption = self.get_best_position(increased_burn)
        result += f'Best position with distance-increased burn: {position}, fuel spent: {fuel_consumption}'
        return result

    def get_best_position(self, fuel_consumption_function: Callable[[int], int]) -> Tuple[int, int]:
        # preprocess data
        max_position = max(self.positions)
        best_position = -1
        best_fuel = fuel_consumption_function(max_position) * len(self.positions)  # can't be possibly bigger than this
        counts: Dict[int, int] = {}
        for i, items in groupby(sorted(self.positions)):
            counts[i] = sum(1 for _ in items)

        # try each possible position
        cache: Dict[int, int] = {}
        for i in range(max_position + 1):
            fuel = 0
            for j in counts:
                distance = i - j if i > j else j - i  # faster than built-in abs()
                consumption = cache.get(distance)
                if consumption is None:
                    consumption = fuel_consumption_function(distance)
                    cache[distance] = consumption
                fuel += (consumption * counts[j])
                if fuel > best_fuel:
                    break  # cannot be the best anymore, no need to continue

            if fuel < best_fuel:
                best_position = i
                best_fuel = fuel

        return best_position, best_fuel


if __name__ == '__main__':
    print(Day07().run())
