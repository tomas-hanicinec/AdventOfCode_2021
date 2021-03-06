from typing import Tuple, NamedTuple, List, Optional, Dict

import utils


class Day22:
    steps: List['RebootStep']

    def __init__(self) -> None:
        self.steps = []
        for line in utils.read_strings('inputs/day_22.txt'):
            on, cube = line.split(' ')
            self.steps.append(RebootStep(on == 'on', parse_dimensions(cube.split(','))))

    def run(self) -> str:
        core = ReactorCore()
        for step in self.steps:
            core.add(step.cube) if step.on else core.remove(step.cube)

        return (
            f'{core.get_active_count(Cuboid((-50, 50), (-50, 50), (-50, 50)))} cubes turned on within the [-50..50] region\n'
            f'{core.get_active_count(None)} cubes turned on in total'
        )


class Cuboid(NamedTuple):
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]


class RebootStep(NamedTuple):
    on: bool
    cube: Cuboid


class ReactorCore:
    cubes: Dict[Cuboid, int]

    def __init__(self) -> None:
        self.cubes = {}

    def add(self, new_cube: Cuboid) -> None:
        # add the new cube and remove all the intersections with current cubes
        new_cubes = {new_cube: 1}
        for cube, weight in self.cubes.items():
            intersection = get_intersection(cube, new_cube)
            if intersection is not None:
                # flip the weight so with "negative" cubes the intersection is added as "positive" and vice versa
                new_cubes[intersection] = new_cubes.get(intersection, 0) - weight
        self.add_new_cubes(new_cubes)

    def remove(self, remove_cube: Cuboid) -> None:
        # remove all the intersections with current cubes
        new_cubes: Dict[Cuboid, int] = {}
        for cube, weight in self.cubes.items():
            intersection = get_intersection(cube, remove_cube)
            if intersection is not None:
                # flip the weight so with "negative" cubes the intersection is added as "positive" and vice versa
                new_cubes[intersection] = new_cubes.get(intersection, 0) - weight
        self.add_new_cubes(new_cubes)

    def add_new_cubes(self, new: Dict[Cuboid, int]) -> None:
        for cube, weight in new.items():
            if weight == 0:
                continue
            current = self.cubes.get(cube, 0)
            if current + weight == 0:
                del self.cubes[cube]
            else:
                self.cubes[cube] = current + weight

    def get_active_count(self, limit: Optional[Cuboid]) -> int:
        result = 0
        for cube, weight in self.cubes.items():
            if limit is not None:
                intersection = get_intersection(cube, limit)
                if intersection is None:
                    continue  # this cube does not fit in the limit
                cube = intersection  # trim the cube according to the given limit
            # add the "positive" cubes, subtract the "negative" ones
            result += weight * (cube.x[1] - cube.x[0] + 1) * (cube.y[1] - cube.y[0] + 1) * (cube.z[1] - cube.z[0] + 1)

        return result


def get_intersection(a: Cuboid, b: Cuboid) -> Optional[Cuboid]:
    # if-else is slightly faster here than max, min
    x_min = a.x[0] if a.x[0] > b.x[0] else b.x[0]
    x_max = a.x[1] if a.x[1] < b.x[1] else b.x[1]
    if x_max < x_min:
        return None

    y_min = max(a.y[0], b.y[0])
    y_max = min(a.y[1], b.y[1])
    if y_max < y_min:
        return None

    z_min = max(a.z[0], b.z[0])
    z_max = min(a.z[1], b.z[1])
    if z_max < z_min:
        return None

    return Cuboid((x_min, x_max), (y_min, y_max), (z_min, z_max))


def parse_dimensions(dimensions: List[str]) -> Cuboid:
    def parse_limits(dimension_limits: str) -> Tuple[int, int]:
        numbers = dimension_limits.split('..')
        a = int(numbers[0])
        b = int(numbers[1])
        return min(a, b), max(a, b)

    limits = [dim.split('=')[1] for dim in dimensions]
    return Cuboid(parse_limits(limits[0]), parse_limits(limits[1]), parse_limits(limits[2]))


if __name__ == '__main__':
    print(Day22().run())
