from typing import List, Set, Tuple

import utils


class Day25:
    sea_floor: 'SeaFloor'

    def __init__(self) -> None:
        self.sea_floor = SeaFloor(utils.read_strings('inputs/day_25.txt'))

    def run(self) -> str:
        new_steps = self.sea_floor.step()
        step_count = 1
        while new_steps > 0:
            new_steps = self.sea_floor.step()
            step_count += 1
        return f'Number of steps before sea cucumbers stop moving: {step_count}'


class SeaFloor:
    map: List[List[str]]
    width: int
    height: int
    cucumbers_east: Set[Tuple[int, int]]
    cucumbers_south: Set[Tuple[int, int]]

    def __init__(self, lines: List[str]) -> None:
        self.map = []
        self.width = len(lines[0])
        self.height = len(lines)
        self.cucumbers_east = set()
        self.cucumbers_south = set()
        for i, line in enumerate(lines):
            self.map.append([x for x in line])
            for j, val in enumerate(line):
                if val == '>':
                    self.cucumbers_east.add((i, j))
                elif val == 'v':
                    self.cucumbers_south.add((i, j))

    def step(self) -> int:
        moves = self.move_east()
        moves += self.move_south()
        return moves

    def move_east(self) -> int:
        moves = {}
        for pos in self.cucumbers_east:
            new_pos = (pos[0], (pos[1] + 1) % self.width)
            if self.map[new_pos[0]][new_pos[1]] == '.':
                moves[pos] = new_pos

        for move_from, move_to in moves.items():
            self.cucumbers_east.remove(move_from)
            self.cucumbers_east.add(move_to)
            self.map[move_from[0]][move_from[1]] = '.'
            self.map[move_to[0]][move_to[1]] = '>'
        return len(moves)

    def move_south(self) -> int:
        moves = {}
        for pos in self.cucumbers_south:
            new_pos = ((pos[0] + 1) % self.height, pos[1])
            if self.map[new_pos[0]][new_pos[1]] == '.':
                moves[pos] = new_pos

        for move_from, move_to in moves.items():
            self.cucumbers_south.remove(move_from)
            self.cucumbers_south.add(move_to)
            self.map[move_from[0]][move_from[1]] = '.'
            self.map[move_to[0]][move_to[1]] = 'v'
        return len(moves)

    def print(self) -> None:
        for row in self.map:
            print(''.join(row))


if __name__ == '__main__':
    print(Day25().run())
