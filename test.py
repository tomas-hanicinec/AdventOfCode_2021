from io import StringIO
from contextlib import redirect_stdout
from day_01 import main as main_01
from day_02 import main as main_02
from day_03 import main as main_03
from day_04 import main as main_04
from day_05 import main as main_05
from day_06 import main as main_06
from day_07 import main as main_07
from day_08 import main as main_08

expected_outputs = (
    '1752 measurements are larger than the previous measurement\n1781 sums that are larger than the previous sum\n',
    'Submarine position (no aim): 1893605\nSubmarine position (with aim): 2120734350\n',
    'Submarine power consumption: 3901196\nSubmarine life support rating: 4412188\n',
    'First winning board score: 74320\nLast winning board score: 17884\n',
    'Overlapping points (straight lines only): 5774\nOverlapping points total: 18423\n',
    'Total number of lantern-fish after 80 days: 352872\nTotal number of lantern-fish after 256 days: 1604361182149\n',
    'Best position with linear burn: 307, fuel spent: 340056\nBest position with distance-increased burn: 460, fuel spent: 96592275\n',
    'Digits {8, 1, 4, 7} appear 367 times in the output\nSum of all the output values: 974512\n'
)


def testDay(day_number, expected):
    day_string = 'DAY {:0>2}:'.format(day_number)
    f = StringIO()
    with redirect_stdout(f):
        eval('main_{:0>2}()'.format(day_number))

    if f.getvalue() != expected:
        print(f'{day_string} FAILED!')
        print(f'Expected:\n{expected}Got:\n{f.getvalue()}')
    else:
        print(f'{day_string} OK')


def main():
    for index, expected in enumerate(expected_outputs):
        testDay(index + 1, expected)


if __name__ == '__main__':
    main()
