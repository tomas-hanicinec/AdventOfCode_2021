from typing import NamedTuple, Tuple, Dict, List

import utils


class Symbol(NamedTuple):
    opening: str
    closing: str
    error_score: int
    autocomplete_value: int


SYMBOLS = (
    Symbol('(', ')', 3, 1),
    Symbol('[', ']', 57, 2),
    Symbol('{', '}', 1197, 3),
    Symbol('<', '>', 25137, 4)
)


class Day10:
    input_lines: List[str]
    symbols: Dict[str, Symbol]

    def __init__(self) -> None:
        self.input_lines = utils.read_strings('inputs/day_10.txt')
        self.symbols = {}

        for symbol in SYMBOLS:
            self.symbols[symbol.opening] = symbol
            self.symbols[symbol.closing] = symbol

    def run(self) -> str:
        error_score_sum = 0
        autocomplete_scores = []
        for line in self.input_lines:
            error_score, autocomplete_score = self.get_scores(line)
            error_score_sum += error_score
            if autocomplete_score != 0:
                autocomplete_scores.append(autocomplete_score)
        autocomplete_scores.sort()

        return (
            f'Total error score: {error_score_sum}\n'
            f'Middle autocomplete score: {autocomplete_scores[len(autocomplete_scores) // 2]}'
        )

    def get_scores(self, line: str) -> Tuple[int, int]:
        stack = [line[0]]
        for char in line[1:]:
            if self.symbols[char].opening == char:
                stack.append(char)  # opening symbol, just add to the stack
                continue

            # closing symbol
            if len(stack) == 0:
                raise Exception(f'invalid input: closing symbol {char} without corresponding opening')
            next_symbol = self.symbols[stack.pop()]
            if char != next_symbol.closing:
                # invalid closing symbol -> error line -> return its error score
                return self.symbols[char].error_score, 0

        # end of the line, calculate autocomplete score (might be 0 if the line is complete)
        autocomplete_score = 0
        stack.reverse()
        for char in stack:
            autocomplete_score = autocomplete_score * 5 + self.symbols[char].autocomplete_value
        return 0, autocomplete_score


if __name__ == '__main__':
    print(Day10().run())
