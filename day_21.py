from itertools import product
from typing import Tuple, Dict

STARTING_POSITIONS = (4, 7)
WINNING_SCORE_DETERMINISTIC = 1000
DICE_SIDES_DETERMINISTIC = 100
WINNING_SCORE_DIRAC = 21
DICE_SIDES_DIRAC = 3

GameCache = Dict[Tuple[bool, Tuple[int, int], Tuple[int, int]], Tuple[int, int]]


class Day21:

    @staticmethod
    def run() -> str:
        losing_score, dice_counter = play_deterministic()
        win_counts = play_dirac()
        return (
            f'Player lost after {dice_counter} deterministic dice rolls with score {losing_score}. Final result: {losing_score * dice_counter}\n'
            f'Winning player wins in {max(win_counts)} universes with Dirac dice'
        )


def play_deterministic() -> Tuple[int, int]:
    dice_counter = 0
    dice_current = 1
    starting_positions = (STARTING_POSITIONS[0] - 1, STARTING_POSITIONS[1] - 1)  # use positions 0-9 instead of 1-10

    positions = starting_positions
    scores = (0, 0)
    game_round = 0
    while max(scores) < WINNING_SCORE_DETERMINISTIC:
        # roll the dice
        dice_result = dice_current + ((dice_current + 1) % DICE_SIDES_DETERMINISTIC) + ((dice_current + 2) % DICE_SIDES_DETERMINISTIC)
        dice_current = ((dice_current + 3) % DICE_SIDES_DETERMINISTIC)
        dice_counter += 3
        # move pieces
        positions, scores = move(game_round, dice_result, positions, scores)
        game_round += 1

    return min(scores), dice_counter


def play_dirac() -> Tuple[int, int]:
    starting_positions = (STARTING_POSITIONS[0] - 1, STARTING_POSITIONS[1] - 1)  # use positions 0-9 instead of 1-10

    # there are 27 possible outcomes of 3 dice rolls, but we only care about their sum (which is way less)
    universe_counts: Dict[int, int] = {}
    for i, j, k in product(range(DICE_SIDES_DIRAC), repeat=3):
        s = i + j + k + 3  # i, j, k start from 0...
        universe_counts[s] = universe_counts[s] + 1 if s in universe_counts else 1

    return play_dirac_round(0, starting_positions, (0, 0), universe_counts, {})


def play_dirac_round(
        game_round: int,
        positions: Tuple[int, int],
        scores: Tuple[int, int],
        universe_counts: Dict[int, int],
        cache: GameCache
) -> Tuple[int, int]:
    if scores[0] >= WINNING_SCORE_DIRAC:
        return 1, 0  # player 1 won in this universe
    if scores[1] >= WINNING_SCORE_DIRAC:
        return 0, 1  # player 2 won in this universe

    game_state = (bool(game_round % 2), positions, scores)
    if game_state in cache:
        return cache[game_state]  # we've already been here, the result will not change so no neet to visit again

    # neither player won yet, we need another round
    player1_wins = player2_wins = 0
    for dice_result in universe_counts:
        new_positions, new_scores = move(game_round, dice_result, positions, scores)
        win1, win2 = play_dirac_round(game_round + 1, new_positions, new_scores, universe_counts, cache)
        player1_wins += universe_counts[dice_result] * win1
        player2_wins += universe_counts[dice_result] * win2

    cache[game_state] = (player1_wins, player2_wins)  # number of possible game states is way lower than the number of all universes, makes sense to cache them
    return player1_wins, player2_wins


def move(
        game_round: int,
        dice_result: int,
        positions: Tuple[int, int],
        scores: Tuple[int, int]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    current_player = game_round % 2  # game rounds start from 0
    new_player_position = (positions[current_player] + dice_result) % 10
    new_player_score = scores[current_player] + new_player_position + 1  # positions are 0-9, use 1-10 for scores
    if current_player == 0:
        return (new_player_position, positions[1]), (new_player_score, scores[1])
    else:
        return (positions[0], new_player_position), (scores[0], new_player_score)


if __name__ == '__main__':
    print(Day21().run())
