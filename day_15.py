from typing import List, Tuple, Dict, Iterator

import utils


class Day15:
    input_lines: List[str]

    def __init__(self) -> None:
        self.input_lines = utils.read_strings('inputs/day_15.txt')

    def run(self) -> str:
        cave_map_small = get_cave_map(self.input_lines, 1)
        path_finder = PathFinder(cave_map_small)
        small_cave_risk = path_finder.run()

        cave_map_big = get_cave_map(self.input_lines, 5)
        path_finder = PathFinder(cave_map_big)

        return (
            f'Lowest total risk for the small cave: {small_cave_risk}\n'
            f'Lowest total risk for the big cave: {path_finder.run()}'
        )


def get_cave_map(lines: List[str], multiplicator: int) -> List[List[int]]:
    result: List[List[int]] = []
    base_size = len(lines[0])
    size = base_size * multiplicator

    for row_i in range(size):
        result.append([0] * size)
        for col_i in range(size):
            batch_row, batch_col = row_i // base_size, col_i // base_size
            increment = batch_row + batch_col  # by how much we must increment the base value in this batch
            base_value = int(lines[row_i - batch_row * base_size][col_i - batch_col * base_size])
            result[row_i][col_i] = ((base_value + increment - 1) % 9) + 1  # increase the value accordingly, 9 loops back to 1 (not 0!)

    return result


class MapPoint:
    x: int
    y: int
    weight: int
    path_length: int

    def __init__(self, x: int, y: int, weight: int, path_length: int) -> None:
        self.x = x
        self.y = y
        self.weight = weight
        self.path_length = path_length


class PathFinder:
    size: int
    max_path_length: int
    points: Dict[Tuple[int, int], MapPoint]  # this is for fast access to the points by their coordinates
    point_queue: List[MapPoint]  # this specifies the order of points we are supposed to visit, it is a subset of self.points

    def __init__(self, cave_map: List[List[int]]):
        self.size = len(cave_map)
        self.max_path_length = self.size * self.size * 9  # risk levels only go to 9 (single-digit)
        self.point_queue = []  # start with empty list, no need to add all the points with max_path_length into it right away

        # init the point map
        self.points = {}
        for y, _ in enumerate(cave_map):
            for x, weight in enumerate(cave_map[y]):
                point = MapPoint(x, y, weight, self.max_path_length)
                self.points[point.x, point.y] = point

    # basically a Dijkstra algorith for shortest graph path
    def run(self) -> int:
        start_point = self.points[(0, 0)]  # start in top left corner
        start_point.path_length = 0  # start weight is not included in the result
        end = (self.size - 1, self.size - 1)  # finish in bottom right corner
        self.point_queue.append(self.points[(0, 0)])  # start with just the start_point, add more points as they are being visited for the first time

        while len(self.point_queue) > 0:
            # process the point with the lowest path_length (first one)
            current_point = self.point_queue.pop(0)
            coordinates = (current_point.x, current_point.y)
            if coordinates == end:
                break  # reached the end, no need to iterate further
            del self.points[coordinates]

            # evaluate the neighbours
            for neighbour_coordinates in self.get_neighbours(coordinates):
                if neighbour_coordinates not in self.points:
                    continue  # this was already processed
                neighbour = self.points[neighbour_coordinates]
                new_neighbour_path_length = current_point.path_length + neighbour.weight
                if new_neighbour_path_length < neighbour.path_length:
                    # found better path, add (or replace) the point in queue
                    self.add_to_queue(neighbour, new_neighbour_path_length)

        return self.points[end].path_length

    def add_to_queue(self, point: MapPoint, new_path_length: int) -> None:
        if point.path_length < self.max_path_length:
            self.point_queue.remove(point)  # point already in queue, remove first

        index = bisect_left(self.point_queue, new_path_length)
        point.path_length = new_path_length
        self.point_queue.insert(index, point)

    def get_neighbours(self, coordinates: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            x, y = coordinates[0] + dx, coordinates[1] + dy
            if 0 <= x < self.size and 0 <= y < self.size:
                yield x, y


def bisect_left(a: List[MapPoint], x: int) -> int:
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid].path_length < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == '__main__':
    print(Day15().run())
