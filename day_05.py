from typing import NamedTuple, Iterator, List

import utils


class Day05:
    vents: List['VentLine']

    def __init__(self) -> None:
        self.vents = [VentLine(i) for i in utils.read_strings('inputs/day_05.txt')]

    def run(self) -> str:
        points = set()
        intersections = set()
        points_straight = set()
        intersections_straight = set()
        for vent in self.vents:
            for point in vent.get_points():
                intersections.add(point) if point in points else None
                points.add(point)
                if not vent.is_diagonal:
                    intersections_straight.add(point) if point in points_straight else None
                    points_straight.add(point)

        return (
            f'Overlapping points (straight lines only): {len(intersections_straight)}\n'
            f'Overlapping points total: {len(intersections)}'
        )


class Point(NamedTuple):
    x: int
    y: int


class VentLine:
    a: Point
    b: Point
    is_diagonal: bool

    def __init__(self, line_definition: str):
        a, b = line_definition.split(' -> ')
        x, y = a.split(',')
        self.a = Point(int(x), int(y))
        x, y = b.split(',')
        self.b = Point(int(x), int(y))
        self.is_diagonal = self.a.x != self.b.x and self.a.y != self.b.y

    def get_points(self) -> Iterator[Point]:
        x_step = self._get_step(self.a.x, self.b.x)
        y_step = self._get_step(self.a.y, self.b.y)
        tl_corner = Point(min(self.a.x, self.b.x), min(self.a.y, self.b.y))
        br_corner = Point(max(self.a.x, self.b.x), max(self.a.y, self.b.y))

        point = self.a
        while br_corner.x >= point.x >= tl_corner.x and br_corner.y >= point.y >= tl_corner.y:
            # while the point is within the vent line, move one point forward
            yield point
            point = Point(point.x + x_step, point.y + y_step)

    @staticmethod
    def _get_step(x1: int, x2: int) -> int:
        if x1 == x2:
            return 0
        return 1 if x1 < x2 else -1


if __name__ == '__main__':
    print(Day05().run())
