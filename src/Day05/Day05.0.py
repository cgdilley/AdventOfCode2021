from __future__ import annotations

from Utility import InputLoader

from typing import Dict, Tuple, List


def main():
    _map: Dict[Tuple[int, int], int] = dict()

    with InputLoader(day=5) as reader:
        for line in reader:
            for coord in Line.parse(line).line():
                if coord in _map:
                    _map[coord] += 1
                else:
                    _map[coord] = 1

    danger = [x for x in _map.values() if x >= 2]

    print(f"DANGEROUS SPOTS: {len(danger)}")


#


#


class Line:

    def __init__(self, c1: Tuple[int, int], c2: Tuple[int, int]):
        self.c1 = c1
        self.c2 = c2

    def line(self) -> List[Tuple[int, int]]:
        if self.c1[0] == self.c2[0]:
            ordered = sorted((self.c1[1], self.c2[1]))
            return [(self.c1[0], y) for y in range(ordered[0], ordered[1] + 1)]
        elif self.c1[1] == self.c2[1]:
            ordered = sorted((self.c1[0], self.c2[0]))
            return [(x, self.c1[1]) for x in range(ordered[0], ordered[1] + 1)]
        return []

    @staticmethod
    def parse(line: str) -> Line:
        return Line(*(tuple(int(x) for x in coord.strip().split(",")) for coord in line.split("->")))


#


if __name__ == '__main__':
    main()
