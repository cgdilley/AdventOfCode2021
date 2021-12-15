from Utility import InputLoader

from Day15.Day15Shared import Cave, binary_insertion, get_path

from typing import Dict, Iterable, List, Set, Tuple, Optional

SCALE = (5, 5)


def main():
    with InputLoader(day=15) as reader:
        cave = Cave.parse(reader)

    original_size = cave.size
    cave.rows = [list(row) for row in [row * SCALE[1] for row in cave.rows] * SCALE[0]]

    for d_row in range(0, SCALE[0]):
        for d_col in range(0, SCALE[1]):
            for row in range(d_row * original_size[0], (d_row + 1) * original_size[0]):
                for col in range(d_col * original_size[1], (d_col + 1) * original_size[1]):
                    cave.rows[row][col] = ((cave.rows[row][col]-1+d_row+d_col) % 9) + 1

    path = get_path(cave)
    print(path)
    print(f"LENGTH = {len(path)}")
    print(f"COST = {sum(cave.rows[r][c] for r, c in path[1:])}")


#


#


if __name__ == '__main__':
    main()
