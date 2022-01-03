from typing import List, NamedTuple, Tuple, Dict, Optional

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HALLWAY_WIDTH = 11
ROOMS = (2, 4, 6, 8)
FINAL_ROOMS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
MAX_POSSIBLE_SCORE = 1000000000
BEST_HEURISTIC_SCORE = 0


class Day23:
    game1: 'Game'
    game2: 'Game'

    def __init__(self) -> None:
        self.game1 = Game(2, '...DC..DC..AB..AB..', '...aa..bb..cc..dd..')
        self.game2 = Game(4, '...DDDC..DCBC..ABAB..AACB..', '...aaaa..bbbb..cccc..dddd..')

    def run(self) -> str:
        return (
            f'Best score folded (2 room depth): {self.get_best_result(self.game1)}\n'
            f'Best score unfolded (4 room depth): {self.get_best_result(self.game2)}'
        )

    @staticmethod
    def get_best_result(game: 'Game') -> int:
        result = find_best_sequence(0, game, MAX_POSSIBLE_SCORE, {})
        if result is None:
            raise Exception('no sequence found')
        best_score, best_sequence = result
        return best_score


class Move(NamedTuple):
    amphipod_type: str
    start: Tuple[int, int]
    end: Tuple[int, int]
    step_count: int
    heuristic_score: int


class Game:
    positions: Dict[Tuple[int, int], str]
    end_state: str
    room_depth: int
    energy_spent: int

    def __init__(self, room_depth: int, start_state: str, end_state: str) -> None:
        self.room_depth = room_depth
        self.end_state = end_state
        self.energy_spent = 0
        self.positions = get_default_positions(room_depth)
        current = 0
        for pos in self.positions:
            self.positions[pos] = start_state[current]
            current += 1

    def get_state(self) -> str:
        return ''.join(self.positions.values())

    def is_finished(self) -> bool:
        return self.get_state() == self.end_state

    def get_score(self) -> int:
        return self.energy_spent
        pass

    def do_move(self, move: Move) -> None:
        self.positions[move.start] = '.'
        amphipod_type = move.amphipod_type
        if move.end[0] == FINAL_ROOMS[move.amphipod_type]:
            amphipod_type = amphipod_type.lower()  # type is lowercase if this is the final position
        self.positions[move.end] = amphipod_type
        self.energy_spent += ENERGY[move.amphipod_type] * move.step_count

    def revert_move(self, move: Move) -> None:
        self.positions[move.end] = '.'
        self.positions[move.start] = move.amphipod_type
        self.energy_spent -= ENERGY[move.amphipod_type] * move.step_count

    def get_moves(self) -> List[Move]:
        moves = []
        for pos in self.positions:
            if self.positions[pos] == '.':
                continue  # nothing here
            if self.positions[pos] in ENERGY:
                # only process amphipods not yet in their final room (uppercase ones)
                moves += self.get_amphipod_moves(pos)

        moves.sort(key=lambda x: x.heuristic_score)
        return moves

    def get_amphipod_moves(self, start: Tuple[int, int]) -> List[Move]:
        amphipod = self.positions[start]
        if start[1] == 0:
            # amphipod is in the hallway, it can only go into its final room
            return self.get_amphipod_hallway_moves(amphipod, start[0])

        # amphipod is in room, it's not the final room -> it can go into the hallway or directly to its final room
        return self.get_amphipod_room_moves(amphipod, start)

    def get_amphipod_hallway_moves(self, amphipod: str, start_x: int) -> List[Move]:
        if not self.is_final_room_free(amphipod):
            return []  # room is not free, this amphipod cannot move anywhere

        final_x = FINAL_ROOMS[amphipod]
        increment = 1 if final_x > start_x else -1
        for x in range(start_x + increment, final_x + increment, increment):
            if self.positions[(x, 0)] != '.':
                return []  # hallway towards the final room is blocked, cannot move there
        # ok, we moved along the hallway above the final room, now go to the bottom of the room
        y = 0
        while y < self.room_depth and self.positions[(final_x, y + 1)] == '.':
            y += 1  # move one step down

        steps = abs(start_x - final_x) + y
        return [Move(amphipod, (start_x, 0), (final_x, y), steps, BEST_HEURISTIC_SCORE)]  # only single move possible for amphipods waiting in the hallway

    def get_amphipod_room_moves(self, amphipod: str, start: Tuple[int, int]) -> List[Move]:
        start_x, start_y = start
        final_x = FINAL_ROOMS[amphipod]

        # first check if we can move from the room at all
        for y in range(start_y - 1, 0, -1):
            if self.positions[(start_x, y)] != '.':
                return []  # way up from the room blocked, cannot move at all
        steps_up = start_y

        # now we're in the hallway above the starting room, we can go left or right
        moves = []
        for iterator in [range(start_x - 1, -1, -1), range(start_x + 1, HALLWAY_WIDTH)]:
            for x in iterator:
                if self.positions[(x, 0)] != '.':
                    break  # hallway blocked at this point, cannot go further
                if x == final_x and self.is_final_room_free(amphipod):
                    # we're above the final room -> go in (and discard other moves, this will always be better)
                    y = 0
                    while y < self.room_depth and self.positions[(final_x, y + 1)] == '.':
                        y += 1  # move one step down
                    steps = steps_up + abs(start_x - x) + y
                    return [Move(amphipod, start, (final_x, y), steps, BEST_HEURISTIC_SCORE)]
                if x in ROOMS:
                    continue  # we're above a room, cannot stop here, go on

                # we can stop here, add to the possible steps
                steps = steps_up + abs(start_x - x)
                heuristic_score = abs(x - final_x) + ENERGY[amphipod] * steps  # the closer we end up to the final room the better, the cheaper the move, the better
                moves.append(Move(amphipod, start, (x, 0), steps, heuristic_score))

        return moves

    def is_final_room_free(self, amphipod: str) -> bool:
        final_room = FINAL_ROOMS[amphipod]
        for i in range(1, self.room_depth + 1):
            if self.positions[(final_room, i)] != '.' and self.positions[(final_room, i)] != amphipod.lower():
                return False  # room blocked by some other amphipod

        return True

    def print(self) -> None:
        strings = []
        for i in range(self.room_depth + 1):
            strings.append([' '] * HALLWAY_WIDTH)
        for pos in self.positions:
            strings[pos[1]][pos[0]] = self.positions[pos]
        for line in strings:
            print(''.join(line))


def find_best_sequence(depth: int, game: Game, best_score_so_far: int, cache: Dict[str, int]) -> Optional[Tuple[int, List[Move]]]:
    current_score = game.get_score()
    if game.is_finished():
        return current_score, []  # we're done, send score, the sequence moves will be filled on the way up

    if current_score >= best_score_so_far:
        return None  # we already have better score, do not waste time here

    state = game.get_state()
    previous_score = cache.get(state)
    if previous_score is not None and previous_score <= current_score:
        return None  # we've already been here, and with better score
    else:
        cache[state] = game.get_score()  # store the new best

    moves = game.get_moves()
    if len(moves) < 1:
        return None

    best_score = MAX_POSSIBLE_SCORE
    best_sequence = []
    best_move = None
    for move in moves:
        game.do_move(move)
        result = find_best_sequence(depth + 1, game, best_score, cache)
        if result is not None:
            score, sequence = result
            if score < best_score:
                best_score = score
                best_sequence = sequence
                best_move = move
        game.revert_move(move)

    if best_move is None or best_sequence is None:
        return None
    return best_score, [best_move] + best_sequence


def get_default_positions(room_depth: int) -> Dict[Tuple[int, int], str]:
    result = {}
    for x in range(HALLWAY_WIDTH):
        result[(x, 0)] = '.'
        if x in ROOMS:
            for y in range(1, room_depth + 1):
                result[(x, y)] = '.'
    return result


if __name__ == '__main__':
    print(Day23().run())
