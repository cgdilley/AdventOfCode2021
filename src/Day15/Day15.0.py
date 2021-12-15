from Utility import InputLoader

from Day15.Day15Shared import Cave, binary_insertion, get_path

from typing import Dict, Iterable, List, Set, Tuple, Optional


def main():
    with InputLoader(day=15) as reader:
        cave = Cave.parse(reader)

    path = get_path(cave)
    print(path)
    print(f"LENGTH = {len(path)}")
    print(f"COST = {sum(cave.rows[r][c] for r, c in path[1:])}")


#


#


if __name__ == '__main__':
    main()
