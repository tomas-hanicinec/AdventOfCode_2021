from io import StringIO
from contextlib import redirect_stdout
import day_01

expected_outputs = (
    '1752 measurements are larger than the previous measurement\n1781 sums that are larger than the previous sum\n',
)


def testDay(day_number, expected):
    day_string = 'DAY {:0>2}:'.format(day_number)
    f = StringIO()
    with redirect_stdout(f):
        call = 'day_{:0>2}.main()'.format(day_number)
        eval(call)

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
