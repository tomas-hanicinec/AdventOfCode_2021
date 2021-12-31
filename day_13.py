from typing import List, Set, Tuple

import utils


class Day13:
    activation_code: 'ActivationCode'
    fold_instructions: List[Tuple[str, int]]
    
    def __init__(self) -> None:
        lines = utils.read_strings('inputs/day_13.txt')
        separator = lines.index('')
        self.activation_code = ActivationCode(lines[:separator])
        self.fold_instructions = []
        for line in lines[separator + 1:]:
            direction, value = line.replace('fold along ', '').split('=')
            self.fold_instructions.append((direction, int(value)))

    def run(self) -> str:
        first_fold_dot_count = None
        for direction, value in self.fold_instructions:
            self.activation_code.fold(direction, value)
            first_fold_dot_count = self.activation_code.dot_count if first_fold_dot_count is None else first_fold_dot_count

        return f'{first_fold_dot_count} dots visible after the first fold\n' + str(self.activation_code)


class ActivationCode:
    _dots: Set[Tuple[int, int]]
    width: int
    height: int

    def __init__(self, lines: List[str]) -> None:
        self._dots = set()
        self.width = 0
        self.height = 0
        for line in lines:
            x, y = (int(n) for n in line.split(','))
            self._dots.add((x, y))
            self.width = max(x, self.width)
            self.height = max(y, self.height)

    def fold(self, direction: str, value: int) -> None:
        new_dots = set()
        for dot in self._dots:
            fold_index = 0 if direction == 'x' else 1
            if dot[fold_index] > value:
                # dot only changes coordinates when on the "far" side of the fold
                new_dot = [0, 0]
                new_dot[fold_index] = 2 * value - dot[fold_index]  # one coordinate changes
                new_dot[1 - fold_index] = dot[1 - fold_index]  # the other one stays the same
                dot = (new_dot[0], new_dot[1])

            new_dots.add(dot)  # add to new dots (either changed or not)
            # handle sizes change
            if direction == 'x':
                self.width = value - 1
            else:
                self.height = value - 1

        self._dots = new_dots  # replace the dots with the folded ones

    @property
    def dot_count(self) -> int:
        return len(self._dots)

    def __str__(self) -> str:
        lines = []
        for i in range(self.height + 1):
            lines.append([' '] * self.width)

        for dot in self._dots:
            lines[dot[1]][dot[0]] = '#'

        return '\n'.join(["".join(line) for line in lines])


if __name__ == '__main__':
    print(Day13().run())
