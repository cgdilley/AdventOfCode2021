from Utility import InputLoader

import re
import math
from typing import Tuple


def main():
    with InputLoader(day=17) as reader:
        line = next(reader)
        match = re.match(r"target area: x=(\d+\.\.\d+), y=(-?\d+\.\.-?\d+)", line)
        x_range = tuple(int(n) for n in match.group(1).split(".."))
        y_range = tuple(int(n) for n in match.group(2).split(".."))

        # This is just so my IDE stops complaining about type mismatches
        x_range = (x_range[0], x_range[1])
        y_range = (y_range[0], y_range[1])

    min_x = get_minimum_x(x_range)
    min_y = get_minimum_y(y_range)
    max_x = get_maximum_x(x_range)
    max_y = get_maximum_y(y_range)

    answers = []
    for xv in range(min_x, max_x + 1):
        for yv in range(min_y, max_y + 1):
            if Probe(0, 0, xv, yv).test_for_range(x_range, y_range):
                answers.append((xv, yv))

    print(answers)
    print(f"TOTAL SOLUTIONS = {len(answers)}")


#


def get_maximum_y(y_range: Tuple[int, int]) -> int:
    return -y_range[0] - 1


def get_minimum_y(y_range: Tuple[int, int]) -> int:
    return y_range[0]


def get_maximum_x(x_range: Tuple[int, int]) -> int:
    return x_range[1]


def get_minimum_x(x_range: Tuple[int, int]) -> int:
    return int(0.5 * ((((8 * x_range[0]) + 1) ** 0.5) - 1))


class Probe:

    def __init__(self, x: int, y: int, xv: int, yv: int):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv

    def move(self):
        self.x += self.xv
        self.y += self.yv
        self.xv = max(0, self.xv-1)
        self.yv -= 1

    def test_for_range(self, x_range: Tuple[int, int], y_range: Tuple[int, int]) -> bool:
        while self.y >= y_range[0]:
            if x_range[0] <= self.x <= x_range[1] and y_range[0] <= self.y <= y_range[1]:
                return True
            self.move()
        return False


#


#


if __name__ == '__main__':
    main()
