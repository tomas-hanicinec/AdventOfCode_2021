from typing import List, Set, Tuple, Dict

import utils


def main() -> None:
    lines = utils.read_strings('inputs/day_11.txt')
    octopus_field = OctopusField(lines)

    solutions_found = 0
    while solutions_found < 2:
        flashes = octopus_field.do_step()

        if octopus_field.step_counter == 100:
            print(f'Number of flashes after 100 steps: {octopus_field.flash_counter}')
            solutions_found += 1

        if flashes == octopus_field.size * octopus_field.size:
            print(f'Number of steps before all octopuses flash: {octopus_field.step_counter}')
            solutions_found += 1


class OctopusField:
    __m: List[List[int]]
    __neighbours: Dict[Tuple[int, int], List[Tuple[int, int]]]
    size: int
    step_counter: int
    flash_counter: int

    def __init__(self, lines: List[str]) -> None:
        self.__m = []
        for line in lines:
            self.__m.append([int(x) for x in line])
        self.size = len(self.__m)
        self.step_counter = 0
        self.flash_counter = 0
        self._init_neighbour_cache()

    def do_step(self) -> int:
        # increase energy for all + find primary flashes
        new_flashes: Set[Tuple[int, int]] = set()
        for i in range(self.size):
            for j in range(self.size):
                self.__m[i][j] += 1
                if self.__m[i][j] > 9:
                    new_flashes.add((i, j))

        # calculate and find secondary flashes
        all_flashes: Set[Tuple[int, int]] = set()
        while len(new_flashes) > 0:
            current_flashes = new_flashes.copy()
            new_flashes = set()

            # first add all the current flashes to the overall set (and reset the energy)
            for point in current_flashes:
                all_flashes.add(point)
                self.__m[point[0]][point[1]] = 0

            # process all the neighbours of all the currently flashing octopuses
            for point in current_flashes:
                for neighbour in self.__neighbours[point]:
                    if neighbour in all_flashes:
                        continue  # this one already flashed in this step
                    self.__m[neighbour[0]][neighbour[1]] += 1
                    if self.__m[neighbour[0]][neighbour[1]] > 9:
                        new_flashes.add(neighbour)  # new flash

        # all flashes done, finish the step
        self.step_counter += 1
        self.flash_counter += len(all_flashes)
        return len(all_flashes)

    def _init_neighbour_cache(self) -> None:
        self.__neighbours = {}
        for i in range(self.size):
            for j in range(self.size):
                self.__neighbours[(i, j)] = self.__get_neighbours(i, j)

    def __get_neighbours(self, x: int, y: int) -> List[Tuple[int, int]]:
        result = []
        for offset in {(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 0), (-1, 1)}:
            p = (x + offset[0], y + offset[1])
            if 0 <= p[0] < self.size and 0 <= p[1] < self.size:
                result.append(p)
        return result


if __name__ == '__main__':
    main()
