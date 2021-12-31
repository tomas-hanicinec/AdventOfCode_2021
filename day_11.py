from itertools import product
from typing import List, Dict, Tuple

import utils


class Day11:
    octopus_field: 'OctopusField'

    def __init__(self) -> None:
        self.octopus_field = OctopusField(utils.read_strings('inputs/day_11.txt'))

    def run(self) -> str:
        result = ['', '']
        solutions_found = 0
        octopus_count = self.octopus_field.size ** 2
        flashes_total = step = 0
        while solutions_found < 2:
            flashes_in_step = self.octopus_field.do_step()
            flashes_total += flashes_in_step
            step += 1

            if step == 100:
                result[0] = f'Number of flashes after 100 steps: {flashes_total}'
                solutions_found += 1
            if flashes_in_step == octopus_count:
                result[1] = f'Number of steps before all octopuses flash: {step}'
                solutions_found += 1

        return '\n'.join(result)


class OctopusField:
    _m: List[List[int]]
    _neighbour_cache: Dict[Tuple[int, int], List[Tuple[int, int]]]
    size: int

    def __init__(self, lines: List[str]) -> None:
        self.size = len(lines)
        self._neighbour_cache = {}
        self._m = []
        for line in lines:
            self._m.append([int(x) for x in line])
        self._init_neighbour_cache()

    def _init_neighbour_cache(self) -> None:
        for i, j in product(range(self.size), range(self.size)):
            self._neighbour_cache[i, j] = []
            for oi, oj in {(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 0), (-1, 1)}:
                pi, pj = i + oi, j + oj
                if 0 <= pi < self.size and 0 <= pj < self.size:
                    self._neighbour_cache[i, j].append((pi, pj))

    def do_step(self) -> int:
        # increase energy for all + find primary flashes
        new_flashes = set()
        for i, j in product(range(self.size), range(self.size)):
            self._m[i][j] += 1
            if self._m[i][j] > 9:
                new_flashes.add((i, j))

        # calculate and find secondary flashes
        all_flashes = set()
        while len(new_flashes) > 0:
            current_flashes = new_flashes.copy()
            new_flashes = set()

            # first add all the current flashes to the overall set (and reset the energy)
            for i, j in current_flashes:
                all_flashes.add((i, j))
                self._m[i][j] = 0

            # process all the neighbours of all the currently flashing octopuses
            for point in current_flashes:
                for i, j in self._neighbour_cache[point]:
                    if (i, j) in all_flashes:
                        continue  # this one already flashed in this step
                    self._m[i][j] += 1
                    if self._m[i][j] > 9:
                        new_flashes.add((i, j))  # new flash

        # all flashes done, finish the step
        return len(all_flashes)


if __name__ == '__main__':
    print(Day11().run())
