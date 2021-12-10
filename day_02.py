from typing import List, Dict, Callable, Tuple

import utils


def main() -> None:
    commands = utils.read_strings('inputs/day_02.txt')

    submarine1 = Submarine(0, 0, 0, 1)
    submarine2 = Submarine(0, 0, 0, 2)
    for command in commands:
        parts = str(command).split(' ')
        submarine1.move(parts[0], int(parts[1]))
        submarine2.move(parts[0], int(parts[1]))

    print(f'Submarine position (no aim): {submarine1.position() * submarine1.depth()}')
    print(f'Submarine position (with aim): {submarine2.position() * submarine2.depth()}')


class Submarine:
    __instruction_map: Dict[str, List[Callable[[int, int], Tuple[int, int, int]]]] = {
        'forward': [
            lambda val, _: (val, 0, 0),
            lambda val, aim: (val, aim * val, 0)
        ],
        'up': [
            lambda val, _: (0, -val, 0),
            lambda val, aim: (0, 0, -val)
        ],
        'down': [
            lambda val, _: (0, val, 0),
            lambda val, aim: (0, 0, val)
        ]
    }
    __position: int
    __depth: int
    __aim: int
    __version: int

    def __init__(self, position: int, depth: int, aim: int, version: int) -> None:
        self.__position = position
        self.__depth = depth
        self.__aim = aim
        self.__version = version

    def move(self, command: str, value: int) -> None:
        command_instructions = self.__instruction_map[command]
        instruction = command_instructions[self.__version - 1]
        d_pos, d_depth, d_aim = instruction(value, self.__aim)
        self.__position += d_pos
        self.__depth += d_depth
        self.__aim += d_aim

    def position(self) -> int:
        return self.__position

    def depth(self) -> int:
        return self.__depth


if __name__ == '__main__':
    main()
