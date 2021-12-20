import math
from typing import NamedTuple, Set, Tuple

import utils


def main() -> None:
    line = utils.read_strings('inputs/day_17.txt')[0]

    line = line.replace('target area: x=', '')
    line = line.replace('y=', '')
    parts = line.split(', ')
    x = [int(n) for n in parts[0].split('..')]
    y = [int(n) for n in parts[1].split('..')]

    target = Target(min(x[0], x[1]), max(x[0], x[1]), min(y[0], y[1]), max(y[0], y[1]))
    if target.min_x <= 0 or target.max_y >= 0:
        raise Exception('target must be positioned to the bottom-right from [0,0]')

    # calculate the bounds for the vertical velocity
    min_x_velocity = math.ceil((math.sqrt(1 + 8 * target.min_x) - 1) / 2)  # any smaller than this and the drag will reduce the forward speed before the target is reached
    max_x_velocity = target.max_x  # any bigger than this and the probe will overshoot the target at t=1 already

    max_height = 0
    solutions: Set[Tuple[int, int]] = set()
    for x_velocity in range(min_x_velocity, max_x_velocity + 1):
        for y_velocity in get_y_velocity(x_velocity, target):
            solutions.add((x_velocity, y_velocity))
            height = get_max_height(y_velocity)
            if height > max_height:
                max_height = height

    print(f'Maximum height reached by the probe: {max_height}')
    print(f'Number of distinct initial velocity vectors: {len(solutions)}')


class Target(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


def get_y_velocity(x_velocity: int, target: Target) -> Set[int]:
    result: Set[int] = set()

    time = 1
    x = get_x(x_velocity, time)
    # keep increasing time until the x-coordinate with this velocity is not behind the target
    while x <= target.max_x:
        if x >= target.min_x:
            # the x-coordinate of the probe is within the target at this time, try to find matching y-coordinates
            y_velocity = target.min_y  # min(target[1]) is the smallest y_velocity that can hit the target (any smaller than this, and it undershoots in t=1)
            y = get_y(y_velocity, time)

            # keep shooting higher while the y-coordinate is not above the target
            while y <= target.max_y:
                if y >= target.min_y:
                    result.add(y_velocity)  # this velocity hits the target, add to the result

                # try shooting higher
                y_velocity += 1
                y = get_y(y_velocity, time)

        # go to the next step
        time += 1
        x = get_x(x_velocity, time)

        if time >= x_velocity + 1:
            # the probe is free-falling within the target x-coordinate since this time, this is tricky as the x stays the same from now on and the outer loop never ends
            for y_velocity in get_y_velocity_for_freefall(x_velocity, target):
                result.add(y_velocity)
            return result

    return result


def get_y_velocity_for_freefall(x_velocity: int, target: Target) -> Set[int]:
    first_freefall_time = x_velocity + 1  # beginning of freefall (we know x-coordinate is within the target from this time on)
    y_velocity = target.min_y  # minimal y-velocity to theoretically hit the target

    result: Set[int] = set()
    while True:
        # get viable time bounds for this velocity
        first_time = get_time(y_velocity, target.max_y)
        last_time = get_time(y_velocity, target.min_y)

        # check them back against the target and add the ones that really hit it
        for time in range(round(first_time), round(last_time) + 1):
            if time < first_freefall_time:
                # probe is not free-falling yet
                # this combination is either off (x-coordinate too low), or it was checked earlier (this function handles free-fall only)
                continue
            y = get_y(y_velocity, time)
            if target.min_y <= y <= target.max_y:
                result.add(y_velocity)  # hitting the target, add to the result

        # with ever-increasing upward velocity, we eventually reach the point where both the time bounds converge to zero y-coordinate
        # this essentially means the gaps between the consecutive time frames are becoming too large to be able to ever hit the target again
        if get_y(y_velocity, first_time) == get_y(y_velocity, last_time) == 0:
            break  # break the loop

        y_velocity += 1  # increase the velocity and try again

    return result


def get_x(x_velocity: int, time: int) -> int:
    drag_time = time - 1
    drag_sum = int((1 + drag_time) * drag_time / 2)
    if drag_time > x_velocity:
        zero_drag = drag_time - x_velocity
        drag_sum -= int((1 + zero_drag) * zero_drag / 2)
    return time * x_velocity - drag_sum


def get_y(y_velocity: int, time: int) -> int:
    gravity_time = time - 1
    gravity_sum = int((1 + gravity_time) * gravity_time / 2)
    return time * y_velocity - gravity_sum


def get_time(y_velocity: int, y: int) -> int:
    # basically an inversion of get_y()
    discriminant = (2 * y_velocity + 1) * (2 * y_velocity + 1) - 8 * y
    time = ((2 * y_velocity + 1) + math.sqrt(discriminant)) / 2
    if time < 0:
        time = ((2 * y_velocity + 1) - math.sqrt(discriminant)) / 2
    return round(time)


def get_max_height(y_velocity: int) -> int:
    gravity_reversal_time = y_velocity + 1
    return get_y(y_velocity, gravity_reversal_time)


if __name__ == '__main__':
    main()
