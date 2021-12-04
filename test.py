from io import StringIO
from contextlib import redirect_stdout
from day_01 import main as main_01
from day_02 import main as main_02
from day_03 import main as main_03
from day_04 import main as main_04

expected_outputs = (
    '1752 measurements are larger than the previous measurement\n1781 sums that are larger than the previous sum\n',
    'Submarine position (no aim): 1893605\nSubmarine position (with aim): 2120734350\n',
    'Submarine power consumption: 3901196\nSubmarine life support rating: 4412188\n',
    'First winning board score: 74320\nLast winning board score: 17884\n'
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
