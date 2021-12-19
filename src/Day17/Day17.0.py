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

    highest_y = get_highest_y(y_range)

    print(f"HIGHEST Y = {highest_y}")


def get_highest_y(y_range: Tuple[int, int]) -> int:
    velocity = -y_range[0] - 1

    return int((velocity * (velocity + 1)) / 2)



#


#


if __name__ == '__main__':
    main()
