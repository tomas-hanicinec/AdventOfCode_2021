from typing import Tuple, List, Dict, Set

import utils

START = 'start'
END = 'end'


def main() -> None:
    lines = utils.read_strings('inputs/day_12.txt')
    links: List[Tuple[str, str]] = []
    for line in lines:
        parts = line.split('-')
        links.append((parts[0], parts[1]))

    cave_map = CaveMap(links)
    path_count_v1, path_count_v2 = cave_map.count_paths()
    print(f'Path count without revisiting small caves: {path_count_v1}')
    print(f'Path count visiting single small cave twice: {path_count_v2}')


class CaveMap:
    __links: Dict[str, List[str]]
    __small_caves: Set[str]
    __path_counter: int

    def __init__(self, links: List[Tuple[str, str]]) -> None:
        self.__links = {}
        self.__small_caves = set()
        for link in links:
            self.__add_link(link[0], link[1])
            self.__add_link(link[1], link[0])

    def __add_link(self, a: str, b: str) -> None:
        if a not in self.__links:
            self.__links[a] = []
        self.__links[a].append(b)
        if a.lower() == a:
            self.__small_caves.add(a)

    def count_paths(self) -> Tuple[int, int]:
        return self.__count_paths([START], False)

    def __count_paths(self, partial_path: List[str], visited_twice: bool) -> Tuple[int, int]:
        start_cave = partial_path[-1]
        if start_cave == END:
            return 1, 1  # path found

        path_count_v1 = path_count_v2 = 0
        for next_cave in self.__links[start_cave]:
            if next_cave in self.__small_caves and next_cave in partial_path:
                # small cave already visited once
                if not visited_twice and next_cave != START:
                    # no small cave visited twice yet (and it's not a start cave) -> add to v2 count
                    _, count2 = self.__count_paths(partial_path + [next_cave], True)
                    path_count_v2 += count2
            else:
                # big cave or unvisited small cave -> add to both v1 and v2
                count1, count2 = self.__count_paths(partial_path + [next_cave], visited_twice)
                path_count_v1 += count1
                path_count_v2 += count2

        return path_count_v1, path_count_v2


if __name__ == '__main__':
    main()
