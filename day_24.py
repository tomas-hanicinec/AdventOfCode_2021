from typing import Dict, List

import utils


class Day24:
    params: List[List[int]]

    def __init__(self) -> None:
        chunk_number = chunk_index = 0
        self.params = [[]]
        for line in utils.read_strings('inputs/day_24.txt')[1:]:
            if line.split(' ')[0] == 'inp':
                chunk_number += 1
                chunk_index = 0
                self.params.append([])
                continue
            if chunk_index == 3 or chunk_index == 4 or chunk_index == 14:
                self.params[chunk_number].append(int(line.split(' ')[2]))
            chunk_index += 1

    def run(self) -> str:
        zs = {'': [0]}
        for depth in range(13, -1, -1):
            new_zs = get_next_zs(zs, self.params[depth])
            zs = new_zs

        max_valid = 0
        min_valid = 99999999999999
        for num in zs:
            valid_number = int(num)
            if max_valid < valid_number:
                max_valid = valid_number
            if min_valid > valid_number:
                min_valid = valid_number

        return (
            f'Maximum valid serial number: {max_valid}\n'
            f'Minimum valid serial number: {min_valid}'
        )


def get_next_zs(previous_zs: Dict[str, List[int]], params: List[int]) -> Dict[str, List[int]]:
    zs = {}
    for n in previous_zs:
        for z in previous_zs[n]:
            for w in range(1, 10):
                key = str(w) + str(n)
                new_zs = get_zs_for_input(params, w, z)
                if len(new_zs) > 0:
                    zs[key] = new_zs

    return zs


def get_zs_for_input(params: List[int], w: int, z: int) -> List[int]:
    c, a, b = params

    if a > 0:
        if (z - w - b) % 26 != 0:
            return []
        return [(z - w - b) // 26]

    res = [z * 26 + w - a]
    for i in range(26):
        new_z = z - w - b - i
        if new_z < 0 or new_z == z - b - a:
            continue
        if 26 * (new_z // 26) != z - w - b:
            continue
        res.append(new_z)
    return res


if __name__ == '__main__':
    print(Day24().run())
