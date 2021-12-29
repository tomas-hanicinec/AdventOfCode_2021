from typing import List, NamedTuple, Tuple, Dict, Optional

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HALLWAY_WIDTH = 11
ROOMS = (2, 4, 6, 8)
FINAL_ROOMS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
MAX_POSSIBLE_SCORE = 1000000000


def main() -> None:
    game = Game(2, '...DC..DC..AB..AB..', '...aa..bb..cc..dd..')
    result = find_best_sequence(0, game, MAX_POSSIBLE_SCORE, {})
    if result is None:
        raise Exception('no sequence found')
    best_score, best_sequence = result
    print(f'Best score folded (2 room depth): {best_score}')

    game = Game(4, '...DDDC..DCBC..ABAB..AACB..', '...aaaa..bbbb..cccc..dddd..')
    result = find_best_sequence(0, game, MAX_POSSIBLE_SCORE, {})
    if result is None:
        raise Exception('no sequence found')
    best_score, best_sequence = result
    print(f'Best score unfolded (4 room depth): {best_score}')


class Move(NamedTuple):
    amphipod_type: str
    start: Tuple[int, int]
    end: Tuple[int, int]
    step_count: int


class Game:

    def __init__(self, room_depth: int, start_state: str, end_state: str) -> None:
        self.room_depth = room_depth
        self.end_state = end_state  # todo - generate end state from FINAL_ROOMS constant
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
        amphipod_type = move.amphipod_type.lower() if move.end[0] == FINAL_ROOMS[move.amphipod_type] else move.amphipod_type
        self.positions[move.end] = amphipod_type  # type is lowercase if this is the final position
        self.energy_spent += ENERGY[move.amphipod_type] * move.step_count

    def revert_move(self, move: Move) -> None:
        self.positions[move.end] = '.'
        self.positions[move.start] = move.amphipod_type
        self.energy_spent -= ENERGY[move.amphipod_type] * move.step_count
        pass

    def get_moves(self) -> List[Move]:
        moves = []
        for pos in self.positions:
            if self.positions[pos] == '.':
                continue  # nothing here
            if self.positions[pos] in ENERGY:
                # only process amphipods not yet in their final room (uppercase ones)
                moves += self.get_amphipod_moves(pos)

        return moves  # todo - order moves by some heuristic

    def get_amphipod_moves(self, pos: Tuple[int, int]) -> List[Move]:
        amphipod = self.positions[pos]
        start = pos

        if pos[1] == 0:
            # amphipod is in the hallway, it can only go into its final room
            if not self.is_final_room_free(amphipod):
                return []  # room is not free, this amphipod cannot move anywhere
            current = start
            final_room = FINAL_ROOMS[amphipod]
            increment = 1 if final_room > current[0] else -1
            while current[0] != final_room:
                current = (current[0] + increment, current[1])
                if self.positions[current] != '.':
                    return []  # hallway towards the final room is blocked, cannot move there
            steps = abs(start[0] - final_room)
            # ok, we moved along the hallway above the final room, now go to the bottom of the room
            while current[1] < self.room_depth and self.positions[(current[0], current[1] + 1)] == '.':
                current = (current[0], current[1] + 1)
                steps += 1  # move one step down

            return [Move(amphipod, start, current, steps)]  # only single move possible for amphipods waiting in the hallway

        # amphipod is in room, it's not the final room
        # it can go into the hallway or directly to its final room
        moves = []
        current = start
        steps = 0
        while current[1] > 0:
            current = (current[0], current[1] - 1)
            if self.positions[current] != '.':
                return []  # way up from the room blocked, cannot move at all
            steps += 1

        # now we're in the hallway above the room, we can go left or right
        start_x = current[0]
        start_steps = steps
        for increment in (-1, 1):
            current = (start_x, current[1])  # reset to the start of the hallway movement
            steps = start_steps
            while 0 < current[0] < HALLWAY_WIDTH - 1:
                current = (current[0] + increment, current[1])
                steps += 1
                if self.positions[current] != '.':
                    break  # hallway blocked at this point, cannot go further
                if current[0] == FINAL_ROOMS[amphipod] and self.is_final_room_free(amphipod):
                    # we're above the final room -> go in (and discard other moves, this will always be better)
                    while current[1] < self.room_depth and self.positions[(current[0], current[1] + 1)] == '.':
                        current = (current[0], current[1] + 1)
                        steps += 1
                    return [Move(amphipod, start, current, steps)]
                if current[0] in ROOMS:
                    continue  # we're above a room, cannot stop here, go on

                moves.append(Move(amphipod, start, current, steps))  # we can stop here, add to the possible steps
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
    main()
