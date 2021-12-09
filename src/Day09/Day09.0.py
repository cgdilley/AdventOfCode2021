
from Utility import InputLoader
from typing import List, Tuple, Optional


with InputLoader(day=9) as reader:
    data = [line for line in reader]


def main():
    low_points = []
    for row in range(len(data)):
        for col in range(len(data[row])):
            if is_low_point(row, col):
                low_points.append(data[row][col])

    risk_level = sum(int(x)+1 for x in low_points)
    print(f"RISK LEVEL = {risk_level}")


#


def is_lower_than(value: int, row: int, col: int):
    return not (0 <= row < len(data)) or \
        not (0 <= col < len(data[row])) or data[row][col] > value


def is_low_point(row: int, col: int):
    return all(is_lower_than(data[row][col], row+y, col+x) for y, x in ((-1, 0), (1, 0), (0, -1), (0, 1)))


#


if __name__ == '__main__':
    main()
