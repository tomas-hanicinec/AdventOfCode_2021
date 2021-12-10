from typing import List, Dict, NamedTuple

import utils


def main() -> None:
    count_map: Dict[Point, List[int]] = dict()
    for input_line in utils.read_strings('inputs/day_05.txt'):
        vent_line = VentLine(input_line)
        for point in vent_line.get_points():
            if point in count_map:
                count_map[point][0] += int(not vent_line.is_diagonal)  # first counter is for straight lines only (1st part)
                count_map[point][1] += 1  # second counter is for all
            else:
                count_map[point] = [int(not vent_line.is_diagonal), 1]  # init (first occurrence of the point)

    counter_straight = counter_all = 0
    for val in count_map.values():
        if val[1] > 1:
            counter_all += 1
            if val[0] > 1:
                counter_straight += 1

    print(f'Overlapping points (straight lines only): {counter_straight}')
    print(f'Overlapping points total: {counter_all}')


class Point(NamedTuple):
    x: int
    y: int


class VentLine:
    a: Point
    b: Point
    is_diagonal: bool

    def __init__(self, line_definition: str):
        points = line_definition.split(' -> ')
        p = points[0].split(',')
        self.a = Point(int(p[0]), int(p[1]))
        p = points[1].split(',')
        self.b = Point(int(p[0]), int(p[1]))
        self.is_diagonal = self.a.x != self.b.x and self.a.y != self.b.y

    def get_points(self) -> List[Point]:
        x_step = self.__get_step(self.a.x, self.b.x)
        y_step = self.__get_step(self.a.y, self.b.y)
        tl_corner = Point(min(self.a.x, self.b.x), min(self.a.y, self.b.y))
        br_corner = Point(max(self.a.x, self.b.x), max(self.a.y, self.b.y))

        result: List[Point] = []
        point = self.a
        while br_corner.x >= point.x >= tl_corner.x and br_corner.y >= point.y >= tl_corner.y:
            # while the point is within the vent line, move one point forward
            result.append(point)
            point = Point(point.x + x_step, point.y + y_step)

        return result

    @staticmethod
    def __get_step(x1: int, x2: int) -> int:
        if x1 == x2:
            return 0
        return 1 if x1 < x2 else -1


if __name__ == '__main__':
    main()
