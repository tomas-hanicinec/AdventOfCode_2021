from typing import Tuple, List, Set

import utils


def main() -> None:
    lines = utils.read_strings('inputs/day_09.txt')
    floor_map = FloorMap(lines)

    risk_level_sum = 0
    basin_sizes = []
    for low_point in floor_map.get_low_points():
        risk_level_sum += 1 + floor_map.get_height(low_point)
        basin_sizes.append(floor_map.get_basin_size(low_point))

    basin_sizes.sort(reverse=True)
    top3_size_product = 1
    for size in basin_sizes[:3]:
        top3_size_product *= size

    print(f'Sum of the low point risk level: {risk_level_sum}')
    print(f'Sizes of three largest basins multiplied: {top3_size_product}')


class FloorMap:
    __m: List[List[int]]
    __rows: int
    __columns: int

    def __init__(self, lines: List[str]) -> None:
        self.__m = []
        for line in lines:
            self.__m.append([int(i) for i in line])

        self.__rows = len(self.__m)
        self.__columns = len(self.__m[0])

    def get_height(self, point: Tuple[int, int]) -> int:
        return self.__m[point[0]][point[1]]

    def get_low_points(self) -> Set[Tuple[int, int]]:
        low_points: Set[Tuple[int, int]] = set()
        for i in range(self.__rows):
            for j in range(self.__columns):
                point = (i, j)
                if self.is_low_point(point):
                    low_points.add(point)
        return low_points

    def is_low_point(self, point: Tuple[int, int]) -> bool:
        for neighbour in self.get_neighbours(point):
            if self.get_height(neighbour) <= self.get_height(point):
                return False
        return True

    def get_neighbours(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours = []
        for offset in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            neighbour = (point[0] + offset[0], point[1] + offset[1])
            if 0 <= neighbour[0] < self.__rows and 0 <= neighbour[1] < self.__columns:
                neighbours.append(neighbour)
        return neighbours

    def get_basin_size(self, point: Tuple[int, int]) -> int:
        to_process = [point]
        basin = set()
        while len(to_process) > 0:
            p = to_process.pop()
            basin.add(p)
            for neighbour in self.get_neighbours(p):
                if neighbour in basin:
                    continue  # don't count twice
                if 9 > self.get_height(neighbour) > self.get_height(p):
                    to_process.append(neighbour)

        return len(basin)


if __name__ == '__main__':
    main()
