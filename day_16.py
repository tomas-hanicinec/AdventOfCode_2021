import math
from typing import List, Tuple, Dict, Callable

import utils


class Day16:
    expression: 'BITSExpression'

    def __init__(self) -> None:
        lines = utils.read_strings('inputs/day_16.txt')
        self.expression = BITSExpression(get_binary_string(lines[0]))

    def run(self) -> str:
        versions, result = self.expression.evaluate()
        return (
            f'Sum of version numbers in expression: {versions}\n'
            f'Expression result: {result}'
        )


def get_binary_string(hex_string: str) -> str:
    scale = 16
    num_of_bits = len(hex_string) * 4
    return bin(int(hex_string, scale))[2:].zfill(num_of_bits)


class BITSExpression:
    literal_value_packet_id = 4
    expr: str

    def __init__(self, expression: str) -> None:
        self.expr = expression

    def evaluate(self) -> Tuple[int, int]:
        versions, result, end = self._evaluate_from_index(0)
        return versions, result

    def _evaluate_from_index(self, start_index: int) -> Tuple[int, int, int]:
        current = start_index
        version_number = int(self.expr[current:current + 3], 2)
        current += 3
        packet_id = int(self.expr[current:current + 3], 2)
        current += 3

        # literal value packet -> just return
        if packet_id == self.literal_value_packet_id:
            value, value_end_index = self._get_literal_value(current)
            return version_number, value, value_end_index

        # subpackets -> process recursively
        length_type_id = int(self.expr[current])
        current += 1
        versions_total = version_number
        results: List[int] = []

        # process subpackets according to the length id
        if length_type_id == 0:
            length = int(self.expr[current:current + 15], 2)
            current = start = current + 15
            while current < start + length:
                versions, result, end = self._evaluate_from_index(current)
                versions_total += versions
                results.append(result)
                current = end
        else:
            count = int(self.expr[current:current + 11], 2)
            current += 11
            for _ in range(count):
                versions, result, end = self._evaluate_from_index(current)
                versions_total += versions
                results.append(result)
                current = end

        result = self._get_result(packet_id, results)
        return versions_total, result, current

    def _get_literal_value(self, start_index: int) -> Tuple[int, int]:
        current = start_index
        value_str = ''
        while self.expr[current] != '0':
            value_str += self.expr[current + 1:current + 5]
            current += 5
        value_str += self.expr[current + 1:current + 5]  # add the last chunk (starting with zero)
        return int(value_str, 2), current + 5

    @staticmethod
    def _get_result(packet_id: int, results: List[int]) -> int:
        mapping: Dict[int, Callable[[List[int]], int]] = {
            0: lambda r: sum(r),
            1: lambda r: math.prod(r),
            2: lambda r: min(r),
            3: lambda r: max(r),
            5: lambda r: 1 if r[0] > r[1] else 0,
            6: lambda r: 1 if r[0] < r[1] else 0,
            7: lambda r: 1 if r[0] == r[1] else 0,
        }
        return mapping[packet_id](results)


if __name__ == '__main__':
    print(Day16().run())
