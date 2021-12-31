from dataclasses import dataclass
from typing import Dict, Callable, List

import utils


@dataclass
class SubmarinePosition:
    distance: int
    depth: int
    aim: int


SubmarinePositionIncrement = SubmarinePosition
InstructionSet = Dict[str, Callable[[int, int], SubmarinePositionIncrement]]


class Day02:
    instruction_set_v1 = {
        'forward': lambda val, _: SubmarinePositionIncrement(val, 0, 0),
        'up': lambda val, _: SubmarinePositionIncrement(0, -val, 0),
        'down': lambda val, _: SubmarinePositionIncrement(0, val, 0),
    }
    instruction_set_v2 = {
        'forward': lambda val, aim: SubmarinePositionIncrement(val, aim * val, 0),
        'up': lambda val, aim: SubmarinePositionIncrement(0, 0, -val),
        'down': lambda val, aim: SubmarinePositionIncrement(0, 0, val),
    }
    commands: List[str]

    def __init__(self) -> None:
        self.commands = utils.read_strings('inputs/day_02.txt')

    def run(self) -> str:
        submarine1 = Submarine(SubmarinePosition(0, 0, 0), self.instruction_set_v1)
        submarine2 = Submarine(SubmarinePosition(0, 0, 0), self.instruction_set_v2)
        for command in self.commands:
            command_name, value = str(command).split(' ')
            submarine1.move(command_name, int(value))
            submarine2.move(command_name, int(value))

        return (
            f'Submarine position (no aim): {submarine1.distance * submarine1.depth}\n'
            f'Submarine position (with aim): {submarine2.distance * submarine2.depth}'
        )


class Submarine:
    _position: SubmarinePosition
    instruction_set: InstructionSet

    def __init__(self, position: SubmarinePosition, instruction_set: InstructionSet) -> None:
        self._position = position
        self.instruction_set = instruction_set

    def move(self, command_name: str, value: int) -> None:
        increment = self.instruction_set[command_name](value, self._position.aim)
        self._position = SubmarinePosition(
            distance=self._position.distance + increment.distance,
            depth=self._position.depth + increment.depth,
            aim=self._position.aim + increment.aim,
        )

    @property
    def distance(self) -> int:
        return self._position.distance

    @property
    def depth(self) -> int:
        return self._position.depth


if __name__ == '__main__':
    print(Day02().run())
