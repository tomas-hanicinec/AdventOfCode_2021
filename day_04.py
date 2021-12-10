from typing import List

import utils

BOARD_SIZE = 5


def main() -> None:
    lines = utils.read_strings('inputs/day_04.txt')
    draw = map(int, lines[0].split(','))

    i = 2  # skip the first blank line
    boards: List[Board] = []
    while i < len(lines):
        boards.append(Board(lines[i:(i + BOARD_SIZE)]))
        i += BOARD_SIZE + 1  # skip the blank line before the next board

    winning_boards_count = 0
    for number in draw:
        for board in boards:
            if board.bingo:
                continue
            board.check(number)
            if board.bingo:
                winning_boards_count += 1
                if winning_boards_count == 1:
                    print(f'First winning board score: {board.score * number}')
                if winning_boards_count == len(boards):
                    print(f'Last winning board score: {board.score * number}')
                    return


class Board:
    bingo: bool
    score: int
    __row_sums: List[int]
    __col_sums: List[int]
    __board: List[List[int]]

    def __init__(self, board_lines: List[str]) -> None:
        self.bingo = False
        self.score = 0
        self.__row_sums = [0] * BOARD_SIZE
        self.__col_sums = [0] * BOARD_SIZE
        self.__board = []
        for i in range(BOARD_SIZE):
            self.__board.append([])
            for val in board_lines[i].split():
                self.score += int(val)
                self.__board[i].append(int(val))

    def check(self, number: int) -> None:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.__board[i][j] == number:
                    self.score -= number
                    self.__row_sums[i] += 1
                    self.__col_sums[j] += 1
                    if self.__row_sums[i] == BOARD_SIZE or self.__col_sums[j] == BOARD_SIZE:
                        self.bingo = True
                    return  # let's say numbers in the single board do not repeat


if __name__ == '__main__':
    main()
