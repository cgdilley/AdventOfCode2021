
from Utility import InputLoader
from typing import List, Tuple, Optional, Iterable, Set


with InputLoader(day=9) as reader:
    data = [line for line in reader]


def main():
    basins = []
    for row, col in get_low_points():
        basins.append(list(basin(row, col, set())))

    basins.sort(key=lambda b: len(b), reverse=True)
    total = len(basins[0]) * len(basins[1]) * len(basins[2])
    print(f"TOTAL = {total}")


#


def is_lower_than(value: int, row: int, col: int) -> bool:
    return not (0 <= row < len(data)) or \
        not (0 <= col < len(data[row])) or data[row][col] > value


DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def is_low_point(row: int, col: int) -> bool:
    return all(is_lower_than(data[row][col], row+dy, col+dx) for dy, dx in DIRECTIONS)


def get_low_points() -> Iterable[Tuple[int, int]]:
    for row in range(len(data)):
        for col in range(len(data[row])):
            if is_low_point(row, col):
                yield row, col


def basin(row: int, col: int, ignore: Set[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    if not (0 <= row < len(data)) or not (0 <= col < len(data[row])) or data[row][col] == "9":
        return []

    ignore.add((row, col))
    yield row, col

    for dy, dx in DIRECTIONS:
        if (row + dy, col + dx) not in ignore:
            yield from basin(row + dy, col + dx, ignore)


#


if __name__ == '__main__':
    main()

