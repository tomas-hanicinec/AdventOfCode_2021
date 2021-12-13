from typing import Set, Tuple, List

import utils


def main() -> None:
    lines = utils.read_strings('inputs/day_13.txt')
    separator = lines.index('')
    activation_code = ActivationCode(lines[:separator])

    first_fold = True
    for line in lines[separator + 1:]:
        line = line.replace('fold along ', '')
        exp = line.split('=')
        activation_code.fold(exp[0], int(exp[1]))
        if first_fold:
            print(f'{activation_code.get_dot_count()} dots visible after the first fold')
            first_fold = False

    activation_code.print()


class ActivationCode:
    __dots: Set[Tuple[int, int]]
    width: int
    height: int

    def __init__(self, lines: List[str]) -> None:
        self.__dots = set()
        self.width = 0
        self.height = 0
        for line in lines:
            exp = line.split(',')
            dot = (int(exp[0]), int(exp[1]))
            self.__dots.add(dot)
            self.width = max(dot[0], self.width)
            self.height = max(dot[1], self.height)

    def fold(self, direction: str, value: int) -> None:
        new_dots: Set[Tuple[int, int]] = set()
        for dot in self.__dots:
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

        self.__dots = new_dots  # replace the dots with the folded ones

    def print(self) -> None:
        lines = []
        for i in range(self.height + 1):
            lines.append([' '] * self.width)

        for dot in self.__dots:
            lines[dot[1]][dot[0]] = '#'

        for line in lines:
            print("".join(line))

    def get_dot_count(self) -> int:
        return len(self.__dots)


if __name__ == '__main__':
    main()
