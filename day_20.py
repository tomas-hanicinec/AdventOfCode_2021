from typing import Dict, Tuple, List

import utils


def main() -> None:
    lines = utils.read_strings('inputs/day_20.txt')

    enhancer = ImageEnhancer(lines[0], lines[2:])
    for step in range(50):
        if step == 2:
            print(f'{enhancer.count_light_pixels()} light pixels after 2 enhancements steps')
        enhancer.enhance()
    print(f'{enhancer.count_light_pixels()} light pixels after 50 enhancements steps')


class ImageEnhancer:
    pixels: Dict[Tuple[int, int], bool]
    algorithm: List[bool]
    x_limits: Tuple[int, int]
    y_limits: Tuple[int, int]
    __current_step: int
    __pixel_value_cache: Dict[Tuple[int, int], bool]

    def __init__(self, algorithm: str, image: List[str]) -> None:
        self.__current_step = 0
        self.algorithm = [True if x == '#' else False for x in algorithm]
        self.y_limits = (0, len(image) - 1)
        self.x_limits = (0, len(image[0]) - 1)
        self.__pixels = {}
        for y, _ in enumerate(image):
            for x, _ in enumerate(image[y]):
                self.__pixels[(x, y)] = True if image[y][x] == '#' else False

    def enhance(self) -> None:
        self.__pixel_value_cache = {}
        self.__current_step += 1
        outside_value = self.get_outside_pixel_value(self.__current_step)

        # expand by 1 in each direction, only the pixels within these limits have to be calculated
        # the (infinite) rest of the pixels all have outside_value in this step and will change uniformly in the next step
        x_limits = (self.x_limits[0] - 1, self.x_limits[1] + 1)
        y_limits = (self.y_limits[0] - 1, self.y_limits[1] + 1)

        # calculate new pixels and replace the old ones
        new_image = {}
        for y in range(y_limits[0], y_limits[1] + 1):
            for x in range(x_limits[0], x_limits[1] + 1):
                new_image[(x, y)] = self.get_next_pixel_value(x, y, outside_value)

        self.__pixels = new_image
        self.x_limits = x_limits
        self.y_limits = y_limits

    def get_outside_pixel_value(self, step: int) -> bool:
        if not self.algorithm[0]:
            return False  # outside pixels start as 0 and never change
        if self.algorithm[-1]:
            return False if step == 1 else True  # outside pixels start as 0, change to 1 in the first step and never change back

        return bool(1 - (step % 2))  # outside pixels start as 0 and keep iterating between 0 and 1

    def get_next_pixel_value(self, pixel_x: int, pixel_y: int, outside_value: bool) -> bool:
        algo_index = 0
        # get the index in the algorithm from the 3x3 box
        for y in range(pixel_y - 1, pixel_y + 2):
            for x in range(pixel_x - 1, pixel_x + 2):
                current_value = self.__pixel_value_cache[(x, y)] if (x, y) in self.__pixel_value_cache else self.get_current_pixel_value(x, y, outside_value)
                algo_index = 2 * algo_index + current_value

        return self.algorithm[algo_index]

    def get_current_pixel_value(self, x: int, y: int, outside_value: bool) -> bool:
        if x < self.x_limits[0] or x > self.x_limits[1] or y < self.y_limits[0] or y > self.y_limits[1]:
            # pixel outside current scope -> use the precalculated value for surrounding pixels
            return outside_value

        self.__pixel_value_cache[(x, y)] = self.__pixels[(x, y)]
        return self.__pixels[(x, y)]  # return the stored value

    def count_light_pixels(self) -> int:
        counter = 0
        for key in self.__pixels:
            if self.__pixels[key]:
                counter += 1
        return counter


if __name__ == '__main__':
    main()
