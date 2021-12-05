import utils


def main():
    count_map = dict()
    for input_line in utils.read_strings('inputs/day_05.txt'):
        vent_line = VentLine(input_line)
        for point in vent_line.get_points():
            if point in count_map:
                count_map[point][0] += int(not vent_line.is_diagonal)  # first counter is for straight lines only (1st part)
                count_map[point][1] += 1  # second counter is for all
            else:
                count_map[point] = [int(not vent_line.is_diagonal), 1]  # init (first occurrence of the point)

    counter_straight = counter_all = 0
    for val in count_map.values():
        if val[1] > 1:
            counter_all += 1
            if val[0] > 1:
                counter_straight += 1

    print(f'Overlapping points (straight lines only): {counter_straight}')
    print(f'Overlapping points total: {counter_all}')


class VentLine:
    def __init__(self, line):
        points = line.split(' -> ')
        self.__a = tuple(int(x) for x in points[0].split(','))
        self.__b = tuple(int(x) for x in points[1].split(','))
        self.is_diagonal = self.__a[0] != self.__b[0] and self.__a[1] != self.__b[1]

    def get_points(self):
        x_step = self.__get_step(self.__a[0], self.__b[0])
        y_step = self.__get_step(self.__a[1], self.__b[1])
        top_left_corner = (min(self.__a[0], self.__b[0]), min(self.__a[1], self.__b[1]))
        bottom_right_corner = (max(self.__a[0], self.__b[0]), max(self.__a[1], self.__b[1]))

        result = []
        point = self.__a
        while self.__is_in_box(point, top_left_corner, bottom_right_corner):
            result.append(point)
            point = (point[0] + x_step, point[1] + y_step)

        return result

    @staticmethod
    def __get_step(x1, x2):
        if x1 == x2:
            return 0
        return 1 if x1 < x2 else -1

    @staticmethod
    def __is_in_box(p, tl, br):
        return br[0] >= p[0] >= tl[0] and br[1] >= p[1] >= tl[1]


if __name__ == '__main__':
    main()
