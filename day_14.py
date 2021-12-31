from typing import Dict

import utils


class Day14:
    formula: 'PolymerFormula'

    def __init__(self) -> None:
        lines = utils.read_strings('inputs/day_14.txt')
        template = lines[0]
        instructions: Dict[str, str] = {}
        for line in lines[2:]:
            pair, insertion = line.split(' -> ')
            instructions[pair] = insertion

        self.formula = PolymerFormula(template, instructions)

    def run(self) -> str:
        result_after_9 = 0
        for i in range(40):
            self.formula.do_step()
            if i == 9:
                result_after_9 = self.formula.get_result()

        return (
            f'Result after 10 steps: {result_after_9}\n'
            f'Result after 40 steps: {self.formula.get_result()}'
        )


class PolymerFormula:
    pair_counts: Dict[str, int]
    element_counts: Dict[str, int]

    def __init__(self, template: str, instructions: Dict[str, str]) -> None:
        self.template = template
        self.instructions = instructions

        self.pair_counts = {}
        self.element_counts = {}
        for i, element in enumerate(self.template):
            self.add_element(element, 1)
            if i + 1 == len(self.template):
                continue  # last element, no more pairs
            self.add_pair(element, self.template[i + 1], 1)

    def do_step(self) -> None:
        pair_counts = self.pair_counts.copy()
        for pair in pair_counts:
            if pair in self.instructions:
                # new element will be added between this pair (for each pair occurrence)
                new_element = self.instructions[pair]
                self.add_element(new_element, pair_counts[pair])  # add element
                self.add_pair(pair[0], new_element, pair_counts[pair])  # add new pairs
                self.add_pair(new_element, pair[1], pair_counts[pair])
                self.pair_counts[pair] -= pair_counts[pair]  # remove the old pair

    def get_result(self) -> int:
        max_count = min_count = 0
        for element in self.element_counts:
            if self.element_counts[element] > max_count:
                max_count = self.element_counts[element]
            if self.element_counts[element] < min_count or min_count == 0:
                min_count = self.element_counts[element]

        return max_count - min_count

    def add_element(self, element: str, count: int) -> None:
        self.element_counts[element] = self.element_counts.get(element, 0) + count

    def add_pair(self, a: str, b: str, count: int) -> None:
        pair = "".join([a, b])
        self.pair_counts[pair] = self.pair_counts.get(pair, 0) + count


if __name__ == '__main__':
    print(Day14().run())
