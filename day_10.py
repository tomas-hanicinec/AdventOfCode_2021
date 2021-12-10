import utils
from typing import NamedTuple


def main():
    lines = utils.read_strings('inputs/day_10.txt')
    symbol_map = get_symbol_map()

    error_score_sum = 0
    autocomplete_scores = []
    for line in lines:
        error_score, autocomplete_score = get_scores(line, symbol_map)
        error_score_sum += error_score
        if autocomplete_score != 0:
            autocomplete_scores.append(autocomplete_score)
    autocomplete_scores.sort()

    print(f'Total error score: {error_score_sum}')
    print(f'Middle autocomplete score: {autocomplete_scores[int(len(autocomplete_scores) / 2)]}')


class Symbol(NamedTuple):
    opening: str
    closing: str
    error_score: int
    autocomplete_value: int


def get_symbol_map():
    symbols = (
        Symbol('(', ')', 3, 1),
        Symbol('[', ']', 57, 2),
        Symbol('{', '}', 1197, 3),
        Symbol('<', '>', 25137, 4)
    )
    symbol_map = dict()
    for symbol in symbols:
        symbol_map[symbol.opening] = symbol
        symbol_map[symbol.closing] = symbol
    return symbol_map


def get_scores(line, symbols):
    stack = [line[0]]
    for i in range(1, len(line)):
        if symbols[line[i]].opening == line[i]:
            stack.append(line[i])  # opening symbol, just add to the stack
            continue

        # closing symbol
        if len(stack) == 0:
            raise Exception(f'invalid input: closing symbol on position {i} without corresponding opening')
        next_symbol = symbols[stack.pop()]
        if line[i] != next_symbol.closing:
            return symbols[line[i]].error_score, 0  # invalid closing symbol -> error line -> return its error score

    # end of the line, calculate autocomplete score (might be 0 if the line is complete)
    autocomplete_score = 0
    stack.reverse()
    for char in stack:
        autocomplete_score = autocomplete_score * 5 + symbols[char].autocomplete_value
    return 0, autocomplete_score


if __name__ == '__main__':
    main()
