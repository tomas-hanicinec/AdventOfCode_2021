import utils


def main():
    commands = utils.read_strings('inputs/day_02.txt')

    submarine1 = Submarine(0, 0, 0, 1)
    submarine2 = Submarine(0, 0, 0, 2)
    for command in commands:
        parts = str(command).split(' ')
        submarine1.move(parts[0], int(parts[1]))
        submarine2.move(parts[0], int(parts[1]))

    print(f'Submarine position (no aim): {submarine1.position() * submarine1.depth()}')
    print(f'Submarine position (with aim): {submarine2.position() * submarine2.depth()}')


class Submarine:
    __instruction_map = {
        'forward': [
            lambda val, _: [val, 0, 0],
            lambda val, aim: [val, aim * val, 0]
        ],
        'up': [
            lambda val, _: [0, -val, 0],
            lambda val, aim: [0, 0, -val]
        ],
        'down': [
            lambda val, _: [0, val, 0],
            lambda val, aim: [0, 0, val]
        ]
    }

    def __init__(self, position, depth, aim, version):
        self.__position = int(position)
        self.__depth = int(depth)
        self.__aim = int(aim)
        self.__version = int(version)

    def move(self, command, value):
        command_instructions = self.__instruction_map[command]
        instruction = command_instructions[self.__version - 1]
        d_pos, d_depth, d_aim = instruction(value, self.__aim)
        self.__position += d_pos
        self.__depth += d_depth
        self.__aim += d_aim

    def position(self):
        return self.__position

    def depth(self):
        return self.__depth


if __name__ == '__main__':
    main()
