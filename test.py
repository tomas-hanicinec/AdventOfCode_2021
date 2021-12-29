from contextlib import redirect_stdout
from io import StringIO

# noinspection PyUnresolvedReferences
from day_01 import main as main_01
# noinspection PyUnresolvedReferences
from day_02 import main as main_02
# noinspection PyUnresolvedReferences
from day_03 import main as main_03
# noinspection PyUnresolvedReferences
from day_04 import main as main_04
# noinspection PyUnresolvedReferences
from day_05 import main as main_05
# noinspection PyUnresolvedReferences
from day_06 import main as main_06
# noinspection PyUnresolvedReferences
from day_07 import main as main_07
# noinspection PyUnresolvedReferences
from day_08 import main as main_08
# noinspection PyUnresolvedReferences
from day_09 import main as main_09
# noinspection PyUnresolvedReferences
from day_10 import main as main_10
# noinspection PyUnresolvedReferences
from day_11 import main as main_11
# noinspection PyUnresolvedReferences
from day_12 import main as main_12
# noinspection PyUnresolvedReferences
from day_13 import main as main_13
# noinspection PyUnresolvedReferences
from day_14 import main as main_14
# noinspection PyUnresolvedReferences
from day_15 import main as main_15
# noinspection PyUnresolvedReferences
from day_16 import main as main_16
# noinspection PyUnresolvedReferences
from day_17 import main as main_17
# noinspection PyUnresolvedReferences
from day_18 import main as main_18
# noinspection PyUnresolvedReferences
from day_19 import main as main_19
# noinspection PyUnresolvedReferences
from day_20 import main as main_20
# noinspection PyUnresolvedReferences
from day_21 import main as main_21
# noinspection PyUnresolvedReferences
from day_22 import main as main_22
# noinspection PyUnresolvedReferences
from day_23 import main as main_23

expected_outputs = (
    '1752 measurements are larger than the previous measurement\n1781 sums that are larger than the previous sum\n',
    'Submarine position (no aim): 1893605\nSubmarine position (with aim): 2120734350\n',
    'Submarine power consumption: 3901196\nSubmarine life support rating: 4412188\n',
    'First winning board score: 74320\nLast winning board score: 17884\n',
    'Overlapping points (straight lines only): 5774\nOverlapping points total: 18423\n',
    'Total number of lantern-fish after 80 days: 352872\nTotal number of lantern-fish after 256 days: 1604361182149\n',
    'Best position with linear burn: 307, fuel spent: 340056\nBest position with distance-increased burn: 460, fuel spent: 96592275\n',
    'Digits {8, 1, 4, 7} appear 367 times in the output\nSum of all the output values: 974512\n',
    'Sum of the low point risk level: 607\nSizes of three largest basins multiplied: 900864\n',
    'Total error score: 278475\nMiddle autocomplete score: 3015539998\n',
    'Number of flashes after 100 steps: 1667\nNumber of steps before all octopuses flash: 488\n',
    'Path count without revisiting small caves: 3495\nPath count visiting single small cave twice: 94849\n',
    '724 dots visible after the first fold\n ##  ###    ## ###  #### ###  #  # #   \n#  # #  #    # #  # #    #  # #  # #   \n#    #  #    # ###  ###  #  # #  # #   \n#    ###     # #  # #    ###  #  # #   \n#  # #    #  # #  # #    # #  #  # #   \n ##  #     ##  ###  #### #  #  ##  ####\n',
    'Result after 10 steps: 2768\nResult after 40 steps: 2914365137499\n',
    'Lowest total risk for the small cave: 410\nLowest total risk for the big cave: 2809\n',
    'Sum of version numbers in expression: 893\nExpression result: 4358595186090\n',
    'Maximum height reached by the probe: 5050\nNumber of distinct initial velocity vectors: 2223\n',
    'Magnitude of the total sum: 4347\nMaximum magnitude from adding two numbers: 4721\n',
    'Scanners detected 512 distinct beacons\nLargest manhattan distance between two scanners: 16802\n',
    '5461 light pixels after 2 enhancements steps\n18226 light pixels after 50 enhancements steps\n',
    'Player lost after 993 deterministic dice rolls with score 900. Final result: 893700\nWinning player wins in 568867175661958 universes with Dirac dice\n',
    '503864 cubes turned on within the [-50..50] region\n1255547543528356 cubes turned on in total\n',
    'Best score folded (2 room depth): 16489\nBest score unfolded (4 room depth): 43413\n',
)


def test_day(day_number: int, expected: str) -> None:
    f = StringIO()
    with redirect_stdout(f):
        eval('main_{:0>2}()'.format(day_number))
    got = f.getvalue()
    f.close()

    if got != expected:
        print('DAY {:0>2}: FAILED!'.format(day_number))
        print('Expected:\n{}Got:\n{}'.format(expected, got))
    else:
        print('DAY {:0>2}: OK'.format(day_number))


def main() -> None:
    for index, expected in enumerate(expected_outputs):
        test_day(index + 1, expected)


if __name__ == '__main__':
    main()
