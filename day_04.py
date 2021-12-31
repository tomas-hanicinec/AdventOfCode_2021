from itertools import product
from typing import List

import utils

BOARD_SIZE = 5


class Day04:
    draw: List[int]
    boards: List['BingoBoard']

    def __init__(self) -> None:
        lines = utils.read_strings('inputs/day_04.txt')
        self.draw = [int(n) for n in lines[0].split(',')]
        self.boards = [BingoBoard(lines[i:(i + BOARD_SIZE)]) for i in range(2, len(lines), BOARD_SIZE + 1)]

    def run(self) -> str:
        winning_board_scores = []
        for number in self.draw:
            for board in self.boards:
                if board.bingo:
                    continue  # skip boards that are already finished
                board.check(number)
                if board.bingo:
                    winning_board_scores.append((board.score, number))

        first_score, first_number = winning_board_scores[0]
        last_score, last_number = winning_board_scores[-1]
        return (
            f'First winning board score: {first_score * first_number}\n'
            f'Last winning board score: {last_score * last_number}'
        )


class BingoBoard:
    _board: List[List[int]]
    _row_sums: List[int]
    _col_sums: List[int]
    score: int
    bingo: bool

    def __init__(self, board_lines: List[str]) -> None:
        self.bingo = False
        self.score = 0
        self._row_sums = [0] * BOARD_SIZE
        self._col_sums = [0] * BOARD_SIZE
        self._board = []
        for i in range(BOARD_SIZE):
            line = [int(n) for n in board_lines[i].split()]
            self.score += sum(line)
            self._board.append(line)

    def check(self, number: int) -> None:
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if self._board[i][j] == number:
                self.score -= number
                self._row_sums[i] += 1
                self._col_sums[j] += 1
                if self._row_sums[i] == BOARD_SIZE or self._col_sums[j] == BOARD_SIZE:
                    self.bingo = True
                return  # let's say numbers in the single board do not repeat


if __name__ == '__main__':
    print(Day04().run())
