from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

import utils


class Day24:
    params: List[Tuple[int, int, int]]

    def __init__(self) -> None:
        # split given instructions to chunks (one for every input instruction)
        # extract the variable params from each chunk (apart from those, each chunk is exactly the same)
        def get_param(instruction: str) -> int:
            return int(instruction.split(' ')[2])

        self.params = []
        lines = utils.read_strings('inputs/day_24.txt')
        for chunk_number in range(14):
            chunk_instructions = lines[18 * chunk_number:18 * chunk_number + 18]
            self.params.append((
                get_param(chunk_instructions[4]),
                get_param(chunk_instructions[5]),
                get_param(chunk_instructions[15]),
            ))

    def run(self) -> str:
        # start with the "final" 0 (meaning a valid serial number) and get all the possible "Z" register values for all the remaining levels
        z_values = {0: {''}}
        for depth in range(13, -1, -1):
            # each iteration fills the z_values with one level of possible Z-values paired with corresponding input values
            new_z_values = get_next_z_values(z_values, self.params[depth][1], self.params[depth][2])
            z_values = new_z_values

        # in the end there is just one possible Z-value - 0 (the initial state of the Z register)
        return (
            f'Maximum valid serial number: {max(z_values[0])}\n'
            f'Minimum valid serial number: {min(z_values[0])}'
        )


def get_next_z_values(previous_z_values: Dict[int, Set[str]], a: int, b: int) -> Dict[int, Set[str]]:
    result = defaultdict(set)
    for previous_z, previous_inputs in previous_z_values.items():
        for previous_input in previous_inputs:
            for current_input_digit in range(1, 10):
                # try all input digits, collect possible Z-values for each digit and store in result
                current_input = str(current_input_digit) + str(previous_input)
                current_z_values = get_z_values_for_input(current_input_digit, previous_z, a, b)
                if current_z_values is not None:
                    for current_z in current_z_values:
                        result[current_z].add(current_input)  # this Z-value is possible with this input too

    # for each Z-value we only need max and min input, trim the rest
    result_reduced = {}
    for z in result:
        result_reduced[z] = {min(result[z]), max(result[z])} if len(result[z]) > 2 else result[z]
    return result_reduced


# gets the possible values of the "Z" register given the input digit for the current level and the Z-value in the previous level
# these equations are painstakingly manually inferred from the ALU program structure and behaviour
def get_z_values_for_input(input_digit: int, previous_z: int, a: int, b: int) -> Optional[List[int]]:
    if a > 0:
        if (previous_z - input_digit - b) % 26 != 0:
            return None
        return [(previous_z - input_digit - b) // 26]

    result = [previous_z * 26 + input_digit - a]
    for i in range(26):
        possible_z = previous_z - input_digit - b - i
        if possible_z < 0 or possible_z == previous_z - b - a:
            continue
        if 26 * (possible_z // 26) != previous_z - input_digit - b:
            continue
        result.append(possible_z)

    return result


if __name__ == '__main__':
    print(Day24().run())
