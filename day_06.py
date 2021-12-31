from typing import Dict, List

import utils

SPAWNING_PERIOD = 7
NEWBORN_SPAWNING_DELAY = 2


class Day06:
    initial_counter: List[int]

    def __init__(self) -> None:
        input_line = utils.read_strings('inputs/day_06.txt')[0]
        self.initial_counter = [0] * SPAWNING_PERIOD  # group fish by their initial timer value
        for fish_timer in input_line.split(','):
            self.initial_counter[int(fish_timer)] += 1

    def run(self) -> str:
        offspring_count_cache: Dict[int, int] = {}  # use the same cache for both cases (faster)

        def count_fish_after(days: int) -> int:
            result = 0
            for timer, count in enumerate(self.initial_counter):
                result += count * (1 + count_offspring(days - timer, offspring_count_cache))
            return result

        return (
            f'Total number of lantern-fish after 80 days: {count_fish_after(80)}\n'
            f'Total number of lantern-fish after 256 days: {count_fish_after(256)}'
        )


# how many offspring is produced by one fish with timer at 0 in days_remaining days (the initial fish excluded)
def count_offspring(days_remaining: int, offspring_count_cache: Dict[int, int]) -> int:
    if days_remaining < 1:
        return 0  # no new offspring possible

    if days_remaining in offspring_count_cache:
        return offspring_count_cache[days_remaining]

    result = 0
    # first new offspring is tomorrow (days_remaining - 1) and then every SPAWNING_PERIOD days there is a new one
    for day in range(days_remaining - 1, -1, -SPAWNING_PERIOD):
        # include the new fish and its own offspring too
        # it takes NEWBORN_SPAWNING_DELAY + SPAWNING_PERIOD days for this new fish to reproduce, we want the day before (counter at 0)
        result += 1 + count_offspring(day - (NEWBORN_SPAWNING_DELAY + SPAWNING_PERIOD - 1), offspring_count_cache)

    offspring_count_cache[days_remaining] = result
    return result


if __name__ == '__main__':
    print(Day06().run())
