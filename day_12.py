from collections import defaultdict
from typing import Tuple, List, Dict, Set

import utils

START = 'start'
END = 'end'


class Day12:
    cave_map: 'CaveMap'

    def __init__(self) -> None:
        self.cave_map = CaveMap(utils.read_strings('inputs/day_12.txt'))

    def run(self) -> str:
        path_count_v1, path_count_v2 = self.cave_map.count_paths()
        return (
            f'Path count without revisiting small caves: {path_count_v1}\n'
            f'Path count visiting single small cave twice: {path_count_v2}'
        )


class CaveMap:
    _links: Dict[str, List[str]]
    _small_caves: Set[str]

    def __init__(self, lines: List[str]) -> None:
        self._links = defaultdict(list)
        self._small_caves = set()
        for line in lines:
            a, b = line.split('-')
            self._links[a].append(b)
            self._links[b].append(a)
            if a.lower() == a:
                self._small_caves.add(a)

    def count_paths(self) -> Tuple[int, int]:
        return self._count_paths([START], False)

    def _count_paths(self, partial_path: List[str], visited_twice: bool) -> Tuple[int, int]:
        start_cave = partial_path[-1]
        if start_cave == END:
            return 1, 1  # path found

        path_count_v1 = path_count_v2 = 0
        for next_cave in self._links[start_cave]:
            if next_cave in self._small_caves and next_cave in partial_path:
                # small cave already visited once
                if not visited_twice and next_cave != START:
                    # no small cave visited twice yet (and it's not a start cave) -> add to v2 count
                    _, count2 = self._count_paths(partial_path + [next_cave], True)
                    path_count_v2 += count2
            else:
                # big cave or unvisited small cave -> add to both v1 and v2
                count1, count2 = self._count_paths(partial_path + [next_cave], visited_twice)
                path_count_v1 += count1
                path_count_v2 += count2

        return path_count_v1, path_count_v2


if __name__ == '__main__':
    print(Day12().run())
