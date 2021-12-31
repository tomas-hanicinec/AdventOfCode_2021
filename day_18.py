from copy import deepcopy
from math import floor, ceil
from typing import Tuple, Optional, List

import utils


class Day18:
    numbers: List['Pair']

    def __init__(self) -> None:
        lines = utils.read_strings('inputs/day_18.txt')
        self.numbers = [Pair.create_from_string(line) for line in lines]

    def run(self) -> str:
        total_sum = deepcopy(self.numbers[0])
        for number in self.numbers[1:]:
            number = deepcopy(number)
            total_sum = total_sum + number

        max_mag = 0
        for i in range(len(self.numbers)):
            for j in range(len(self.numbers)):
                if i != j:
                    res = deepcopy(self.numbers[i]) + deepcopy(self.numbers[j])
                    res_mag = res.get_magnitude()
                    if res_mag > max_mag:
                        max_mag = res_mag
        return (
            f'Magnitude of the total sum: {total_sum.get_magnitude()}\n'
            f'Maximum magnitude from adding two numbers: {max_mag}'
        )


class SnailfishNumber:

    def to_string(self) -> str:
        pass

    def get_magnitude(self) -> int:
        pass

    def split(self) -> Tuple[Optional['Pair'], bool]:
        pass

    def explode(self, depth: int) -> Tuple[Optional[int], Optional[int], bool]:
        pass

    def place(self, level: int, number: int, direction: int) -> None:
        pass

    def get_pair(self) -> Tuple[int, int]:
        pass

    def get_number(self) -> int:
        pass


class Pair(SnailfishNumber):
    pair: Tuple[SnailfishNumber, SnailfishNumber]

    def __init__(self, left: SnailfishNumber, right: SnailfishNumber):
        self.pair = (left, right)
        super().__init__()

    @staticmethod
    def create_from_string(string: str) -> 'Pair':
        number, end = number_from_string(string, 0)
        return number

    def to_string(self) -> str:
        return '[' + self.pair[0].to_string() + ',' + self.pair[1].to_string() + ']'

    def __add__(self, other: 'Pair') -> 'Pair':
        result = Pair(self, other)  # add the numbers
        # reduce the result
        number_reduced = False
        while not number_reduced:
            _, _, exploded = result.explode(0)
            if exploded:
                continue
            _, split = result.split()
            if split:
                continue
            number_reduced = True

        return result

    def get_magnitude(self) -> int:
        return 3 * self.pair[0].get_magnitude() + 2 * self.pair[1].get_magnitude()

    def split(self) -> Tuple[Optional['Pair'], bool]:
        for i in range(2):
            new_pair, is_split = self.pair[i].split()
            if is_split:
                if new_pair is not None:
                    self.pair = (new_pair, self.pair[1]) if i == 0 else (self.pair[0], new_pair)  # replace current pair
                return None, True
        return None, False

    def explode(self, depth: int) -> Tuple[Optional[int], Optional[int], bool]:
        for i in range(2):
            if isinstance(self.pair[i], Regular):
                continue  # don't care about regular numbers

            # pair[i] is another pair, and it's too deep -> explode it
            assert isinstance(self.pair[i], Pair)
            if depth == 3:
                place_pair = self.pair[i].get_pair()  # [self.pair[i].pair[0].number, self.pair[i].pair[1].number]
                self.pair = (Regular(0), self.pair[1]) if i == 0 else (self.pair[0], Regular(0))  # replace the exploded pair with 0
                self.place(0, place_pair[1 - i], 1 - i)  # place one number from the place_pair on this level (to the other side than the exploded pair)
                return place_pair[i], i, True  # send the second number to place to the parent (along with the direction)

            # not deep enough, check the next level
            number_to_place, direction_to_place, did_explode = self.pair[i].explode(depth + 1)
            if not did_explode:
                continue  # no explosion here, try another child

            if number_to_place is not None and direction_to_place is not None and direction_to_place != i:
                # we need to place a number, and we can do it here -> do it, and we're done
                self.place(0, number_to_place, direction_to_place)
                return None, None, did_explode

            # pass all the stuff we have to the parent
            return number_to_place, direction_to_place, did_explode

        return None, None, False  # this number is either just 2 integers, or there was no explosion in the children

    def place(self, depth: int, number: int, direction: int) -> None:
        # changing direction in the first level
        # if we're placing number to the right, and the right item is a nested pair, we want to place the number to the left there
        children_direction = 1 - direction if depth == 0 else direction
        self.pair[direction].place(depth + 1, number, children_direction)

    def get_pair(self) -> Tuple[int, int]:
        return self.pair[0].get_number(), self.pair[1].get_number()


class Regular(SnailfishNumber):
    number: int

    def __init__(self, number: int):
        self.number = number
        super().__init__()

    def to_string(self) -> str:
        return str(self.number)

    def get_magnitude(self) -> int:
        return self.number

    def split(self) -> Tuple[Optional[Pair], bool]:
        if self.number > 9:
            return Pair(Regular(floor(self.number / 2)), Regular(ceil(self.number / 2))), True
        return None, False

    def place(self, depth: int, number: int, direction: int) -> None:
        self.number += number

    def get_number(self) -> int:
        return self.number


def number_from_string(string: str, number_start: int) -> Tuple[Pair, int]:
    def parse_plain_number(start: int, end_char: str) -> Tuple[SnailfishNumber, int]:
        index = start
        number = ''
        while string[index] != end_char:
            number += string[index]
            index += 1
        return Regular(int(number)), index + 1

    i = number_start + 1  # string[number_start] is always "["
    left: SnailfishNumber
    if string[i] == '[':
        left, i = number_from_string(string, i)  # pair on the left
    else:
        left, i = parse_plain_number(i, ',')  # regular number on the left

    right: SnailfishNumber
    if string[i] == '[':
        right, i = number_from_string(string, i)  # pair on the right
    else:
        right, i = parse_plain_number(i, ']')  # regular number on the right

    return Pair(left, right), i + 1


if __name__ == '__main__':
    print(Day18().run())
