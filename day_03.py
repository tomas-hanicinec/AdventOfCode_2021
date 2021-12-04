import utils


def main():
    number_strings = utils.read_strings('inputs/day_03.txt')

    gamma_rate = epsilon_rate = 0
    for i in range(len(number_strings[0])):
        most_common = get_most_common_bit(number_strings, i)
        gamma_rate = (gamma_rate << 1) + most_common
        epsilon_rate = (epsilon_rate << 1) + 1 - most_common

    print(f'Submarine power consumption: {gamma_rate * epsilon_rate}')

    o2_generator_rating = filter_by_criteria(
        number_strings,
        lambda index, most_common_bit: lambda number_string: int(number_string[index]) == most_common_bit
    )
    co2_scrubber_rating = filter_by_criteria(
        number_strings,
        lambda index, most_common_bit: lambda number_string: int(number_string[index]) != most_common_bit
    )

    print(f'Submarine life support rating: {o2_generator_rating * co2_scrubber_rating}')


def get_most_common_bit(number_strings, position):
    bit_sum = 0
    for number_string in number_strings:
        bit_sum += int(number_string[position])

    remainder = len(number_strings) - bit_sum
    return 0 if bit_sum < remainder else 1


def filter_by_criteria(number_strings, filter_factory):
    remaining = number_strings
    i = 0
    while len(remaining) != 1:
        most_common = get_most_common_bit(remaining, i)
        itr = filter(filter_factory(i, most_common), remaining)
        remaining = list(itr)
        i += 1

    return int(remaining[0], 2)


if __name__ == '__main__':
    main()
