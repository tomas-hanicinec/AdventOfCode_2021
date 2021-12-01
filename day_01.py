import utils


def countIncreases(depths, window_size):
    # calculate the first window sum
    previous_sum = 0
    for depth in depths[0:window_size]:
        previous_sum += depth

    # loop through the rest of the input, count increases
    result = 0
    index = window_size
    while index < len(depths):
        current_sum = previous_sum + depths[index] - depths[index - window_size]  # slide the window forward
        if current_sum > previous_sum:
            result += 1

        previous_sum = current_sum
        index += 1

    return result


def main():
    depths = utils.readIntegers('inputs/day_01.txt')
    print(f'{countIncreases(depths, 1)} measurements are larger than the previous measurement.')
    print(f'{countIncreases(depths, 3)} sums that are larger than the previous sum.')


if __name__ == '__main__':
    main()
