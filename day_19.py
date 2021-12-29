from collections import defaultdict
from itertools import product
from typing import Tuple, List, Dict, Callable, Optional, Set

import utils


def main() -> None:
    # read scanners and beacons from files
    lines = utils.read_strings('inputs/day_19.txt')
    scanners = []
    scanner_id = 0
    scanner_beacons: List[Point] = []
    for line in lines:
        if line[0:3] == '---':
            continue  # scanner header
        if line == '':
            # end of scanner, add to list
            scanners.append(Scanner(scanner_id, scanner_beacons))
            scanner_beacons = []
            scanner_id += 1
            continue
        coords = line.split(',')
        scanner_beacons.append((int(coords[0]), int(coords[1]), int(coords[2])))
    scanners.append(Scanner(scanner_id, scanner_beacons))  # append the last scanner (no newline at the end)

    # identify overlapping (matched) scanners (each scanner should overlap with at least one other scanner)
    matched = {0}
    queue = {0}
    while len(matched) < len(scanners) and len(queue) > 0:
        i = queue.pop()
        for j, _ in enumerate(scanners):
            if j in matched:
                continue  # scanners i and j are already matched
            rotation, offset = get_scanners_position(scanners[i], scanners[j])
            if rotation is None or offset is None:
                continue  # scanner j cannot be matched to scanner i (not enough overlap)
            # found new matched scanner, adjust its position to the calculated one
            scanners[j].set_offsets(rotation, offset, i)
            matched.add(j)
            queue.add(j)
    if len(matched) < len(scanners):
        raise Exception(f'could only match {len(matched)} scanners, not enough overlap in the input')

    # count all distinct beacons
    beacons_union: Set[Point] = set()
    for i, _ in enumerate(scanners):
        beacons = get_beacons_absolute(scanners, i)
        beacons_union = beacons_union.union(beacons)
    print(f'Scanners detected {len(beacons_union)} distinct beacons')

    # get the biggest manhattan distance between scanners
    largest = 0
    for i, _ in enumerate(scanners):
        for j in range(i + 1, len(scanners)):
            oa = get_offset_absolute(scanners, i)
            ob = get_offset_absolute(scanners, j)
            dist = abs(oa[0] - ob[0]) + abs(oa[1] - ob[1]) + abs(oa[2] - ob[2])
            if dist > largest:
                largest = dist
    print(f'Largest manhattan distance between two scanners: {largest}')


Point = Tuple[int, int, int]
Distances = Dict[Tuple[int, int], Point]  # key is the tuple of beacon indexes, value is the (3D) distance between the beacon pair
BeaconPair = Tuple[int, int]
BeaconDistanceMatch = Tuple[BeaconPair, BeaconPair]  # two beacon pairs (from different scanners) whose distances match each other


class Scanner:
    id: int
    beacons: List[Point]
    rotation_id: int
    offset: Tuple[int, int, int]
    reference: int

    def __init__(self, scanner_id: int, beacons: List[Point]) -> None:
        self.id = scanner_id
        self.beacons = beacons
        self.rotation_id = 0
        self.offset = (0, 0, 0)
        self.reference = 0

    def set_offsets(self, rotation_id: int, offset: Point, reference_index: int) -> None:
        self.rotation_id = rotation_id
        self.offset = offset
        self.reference = reference_index
        return

    def get_beacons_absolute(self) -> List[Point]:
        return [move(rotate(x, self.rotation_id), self.offset) for x in self.beacons]


def translate_point(point: Point, rotation_id: int, offset: Point) -> Point:
    return move(rotate(point, rotation_id), offset)


def get_offset_absolute(scanners: List[Scanner], i: int) -> Point:
    offset = (0, 0, 0)
    ref_sc = scanners[i]
    while True:
        offset = translate_point(offset, ref_sc.rotation_id, ref_sc.offset)
        if ref_sc.reference == 0:
            break
        ref_sc = scanners[ref_sc.reference]
    return offset


def get_beacons_absolute(scanners: List[Scanner], i: int) -> List[Point]:
    beacons = scanners[i].beacons
    ref_sc = scanners[i]
    while True:
        new_beacons = []
        for j, b in enumerate(beacons):
            new_beacons.append(translate_point(b, ref_sc.rotation_id, ref_sc.offset))
        beacons = new_beacons
        if ref_sc.reference == 0:
            break
        ref_sc = scanners[ref_sc.reference]

    return beacons


def move(point: Point, offset: Point) -> Point:
    return point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]


def get_scanners_position(a: Scanner, b: Scanner) -> Tuple[Optional[int], Optional[Point]]:
    # 12 items form 66 distinct pairs, they must all be present in matches, otherwise these two scanners do not overlap enough
    matches = match_by_distance(a, b)
    if len(matches) < 66:
        return None, None
    # fortunately the overlaps are distinct enough in the input, otherwise we would have to handle cases with len > 66

    # get mapping of the intersecting beacons
    beacon_map = get_beacon_map(matches)

    # use the mapped beacons to calculate rotation and offset of the scanner b against the scanner a
    for rotation_id in range(24):
        offset = None
        for beacon_index in beacon_map:
            ba = a.beacons[beacon_index]
            bb = b.beacons[beacon_map[beacon_index]]
            # we know ba and bb are the same beacon, just differently positioned and rotated
            bb_rotated = rotate(bb, rotation_id)  # try this rotation and calculate offset
            beacon_offset = (ba[0] - bb_rotated[0], ba[1] - bb_rotated[1], ba[2] - bb_rotated[2])
            offset = offset if offset is not None else beacon_offset
            if offset != beacon_offset:
                # offset between ba and bb must be the same as all the previous offsets (if not, this rotation is not the correct one)
                offset = None
                break
        if offset is not None:
            return rotation_id, offset  # found the correct rotation and offset

    raise Exception(f'no possible rotation found for scanners {a.id} and {b.id}')


# matches the given dictionaries by their value, outputs the list of tuples containing matching keys
def match_by_distance(a: Scanner, b: Scanner) -> List[BeaconDistanceMatch]:
    da = get_distances(a)
    db = get_distances(b)

    map_a: Dict[Point, Set[BeaconPair]] = defaultdict(set)
    map_b: Dict[Point, Set[BeaconPair]] = defaultdict(set)
    for beacon_pair, distance in da.items():
        map_a[distance].add(beacon_pair)
    for beacon_pair, distance in db.items():
        map_b[distance].add(beacon_pair)

    matches = []
    for distance in map_a:
        if distance in map_b:
            for prod in product(map_a[distance], map_b[distance]):
                matches.append(prod)
    return matches


# calculate normalized distance (in all 3 coordinates) for every pair of scanner beacons
def get_distances(scanner: Scanner) -> Distances:
    def get_distance(a: Point, b: Point) -> Point:
        return abs(b[0] - a[0]), abs(b[1] - a[1]), abs(b[2] - a[2])

    distances = {}
    for i, _ in enumerate(scanner.beacons):
        for j in range(i + 1, len(scanner.beacons)):
            distance = get_distance(scanner.beacons[i], scanner.beacons[j])
            normalized = sorted(distance)
            distances[(i, j)] = (normalized[0], normalized[1], normalized[2])

    return distances


def get_beacon_map(matches: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Dict[int, int]:
    options_map: Dict[int, Set[int]] = {}
    beacon_map: Dict[int, int] = {}
    for match in matches:
        options = set(match[1])
        for beacon_index in match[0]:
            if beacon_index in beacon_map:
                continue  # this beacon is already mapped to a single value
            if beacon_index in options_map:
                # already mapped to an options set, reduce to a single index value (intersection should never yield more values here)
                beacon_map[beacon_index] = options_map[beacon_index].intersection(options).pop()
                del options_map[beacon_index]
            options_map[beacon_index] = options  # this beacon is not yet mapped, map to all the possible options
    if len(beacon_map) < 12:
        raise Exception('invalid input, beacon map could not be created')
    return beacon_map


# there are 24 specific ways of how a scanner can be rotated / flipped against the reference (first) scanner
# copied from someone else's solution, did not have enough mental capacity to enumerate this crap correctly...
def rotate(point: Point, rotation_id: int) -> Point:
    rotation_map: Dict[int, Callable[[Point], Point]] = {
        0: lambda p: (+p[0], +p[1], +p[2]),
        1: lambda p: (+p[0], -p[2], +p[1]),
        2: lambda p: (+p[0], -p[1], -p[2]),
        3: lambda p: (+p[0], +p[2], -p[1]),

        4: lambda p: (-p[0], -p[1], +p[2]),
        5: lambda p: (-p[0], +p[2], +p[1]),
        6: lambda p: (-p[0], +p[1], -p[2]),
        7: lambda p: (-p[0], -p[2], -p[1]),

        8: lambda p: (+p[1], +p[2], +p[0]),
        9: lambda p: (+p[1], -p[0], +p[2]),
        10: lambda p: (+p[1], -p[2], -p[0]),
        11: lambda p: (+p[1], +p[0], -p[2]),

        12: lambda p: (-p[1], -p[2], +p[0]),
        13: lambda p: (-p[1], +p[0], +p[2]),
        14: lambda p: (-p[1], +p[2], -p[0]),
        15: lambda p: (-p[1], -p[0], -p[2]),

        16: lambda p: (+p[2], +p[0], +p[1]),
        17: lambda p: (+p[2], -p[1], +p[0]),
        18: lambda p: (+p[2], -p[0], -p[1]),
        19: lambda p: (+p[2], +p[1], -p[0]),

        20: lambda p: (-p[2], -p[0], +p[1]),
        21: lambda p: (-p[2], +p[1], +p[0]),
        22: lambda p: (-p[2], +p[0], -p[1]),
        23: lambda p: (-p[2], -p[1], -p[0])
    }
    return rotation_map[rotation_id](point)


if __name__ == '__main__':
    main()
