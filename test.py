import time

from day_01 import Day01
from day_02 import Day02
from day_03 import Day03
from day_04 import Day04
from day_05 import Day05
from day_06 import Day06
from day_07 import Day07
from day_08 import Day08
from day_09 import Day09
from day_10 import Day10
from day_11 import Day11
from day_12 import Day12
from day_13 import Day13
from day_14 import Day14
from day_15 import Day15
from day_16 import Day16
from day_17 import Day17
from day_18 import Day18
from day_19 import Day19
from day_20 import Day20
from day_21 import Day21
from day_22 import Day22
from day_23 import Day23
from day_24 import Day24
from day_25 import Day25

expected_outputs = {
    Day01.__name__: '1752 measurements are larger than the previous measurement\n1781 sums that are larger than the previous sum',
    Day02.__name__: 'Submarine position (no aim): 1893605\nSubmarine position (with aim): 2120734350',
    Day03.__name__: 'Submarine power consumption: 3901196\nSubmarine life support rating: 4412188',
    Day04.__name__: 'First winning board score: 74320\nLast winning board score: 17884',
    Day05.__name__: 'Overlapping points (straight lines only): 5774\nOverlapping points total: 18423',
    Day06.__name__: 'Total number of lantern-fish after 80 days: 352872\nTotal number of lantern-fish after 256 days: 1604361182149',
    Day07.__name__: 'Best position with linear burn: 307, fuel spent: 340056\nBest position with distance-increased burn: 460, fuel spent: 96592275',
    Day08.__name__: 'Digits {8, 1, 4, 7} appear 367 times in the output\nSum of all the output values: 974512',
    Day09.__name__: 'Sum of the low point risk level: 607\nSizes of three largest basins multiplied: 900864',
    Day10.__name__: 'Total error score: 278475\nMiddle autocomplete score: 3015539998',
    Day11.__name__: 'Number of flashes after 100 steps: 1667\nNumber of steps before all octopuses flash: 488',
    Day12.__name__: 'Path count without revisiting small caves: 3495\nPath count visiting single small cave twice: 94849',
    Day13.__name__: '724 dots visible after the first fold\n ##  ###    ## ###  #### ###  #  # #   \n#  # #  #    # #  # #    #  # #  # #   \n#    #  #    # ###  ###  #  # #  # #   \n#    ###     # #  # #    ###  #  # #   \n#  # #    #  # #  # #    # #  #  # #   \n ##  #     ##  ###  #### #  #  ##  ####',
    Day14.__name__: 'Result after 10 steps: 2768\nResult after 40 steps: 2914365137499',
    Day15.__name__: 'Lowest total risk for the small cave: 410\nLowest total risk for the big cave: 2809',
    Day16.__name__: 'Sum of version numbers in expression: 893\nExpression result: 4358595186090',
    Day17.__name__: 'Maximum height reached by the probe: 5050\nNumber of distinct initial velocity vectors: 2223',
    Day18.__name__: 'Magnitude of the total sum: 4347\nMaximum magnitude from adding two numbers: 4721',
    Day19.__name__: 'Scanners detected 512 distinct beacons\nLargest manhattan distance between two scanners: 16802',
    Day20.__name__: '5461 light pixels after 2 enhancements steps\n18226 light pixels after 50 enhancements steps',
    Day21.__name__: 'Player lost after 993 deterministic dice rolls with score 900. Final result: 893700\nWinning player wins in 568867175661958 universes with Dirac dice',
    Day22.__name__: '503864 cubes turned on within the [-50..50] region\n1255547543528356 cubes turned on in total',
    Day23.__name__: 'Best score folded (2 room depth): 16489\nBest score unfolded (4 room depth): 43413',
    Day24.__name__: 'Maximum valid serial number: 91398299697996\nMinimum valid serial number: 41171183141291',
    Day25.__name__: 'Number of steps before sea cucumbers stop moving: 532',
}


def run_all() -> None:
    start = time.time()

    for classname, expected in expected_outputs.items():
        day_start = time.time()
        day_constructor = globals()[classname]
        day_instance = day_constructor()
        got = day_instance.run()
        if got != expected:
            print(f'{classname}: FAILED!')
            print(f'Expected:\n{expected}\nGot:\n{got}\n')
        else:
            print(f'{classname}: OK', '({:.3f} s)'.format(time.time() - day_start))

    print('---------------------------------')
    print(f'total time: {round(time.time() - start, 2)} seconds')


if __name__ == '__main__':
    run_all()
