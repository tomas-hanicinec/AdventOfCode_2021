import utils

SPAWNING_PERIOD = 7
NEWBORN_SPAWNING_DELAY = 2
offspring_count_cache = {}


def main():
    input_line = utils.read_strings('inputs/day_06.txt')[0]

    counter = [0] * SPAWNING_PERIOD
    for fish_timer in input_line.split(','):
        counter[int(fish_timer)] += 1

    def count_fish_after(days):
        result = 0
        for timer, count in enumerate(counter):
            result += count * (1 + count_offspring(days - timer))
        return result

    print(f'Total number of lantern-fish after 80 days: {count_fish_after(80)}')
    print(f'Total number of lantern-fish after 256 days: {count_fish_after(256)}')


# how many offspring is produced by one fish with timer at 0 in days_remaining days (the initial fish excluded)
def count_offspring(days_remaining):
    if days_remaining < 1:
        return 0  # no new offspring possible

    if days_remaining in offspring_count_cache:
        return offspring_count_cache[days_remaining]

    result = 0
    # first new offspring is tomorrow (days_remaining - 1) and then every SPAWNING_PERIOD days there is a new one
    for day in range(days_remaining - 1, -1, -SPAWNING_PERIOD):
        # include the new fish and its own offspring too
        # it takes NEWBORN_SPAWNING_DELAY + SPAWNING_PERIOD days for this new fish to reproduce, we want the day before (counter at 0)
        result += 1 + count_offspring(day - (NEWBORN_SPAWNING_DELAY + SPAWNING_PERIOD - 1))

    offspring_count_cache[days_remaining] = result
    return result


if __name__ == '__main__':
    main()
