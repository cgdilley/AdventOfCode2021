from __future__ import annotations

from Utility import InputLoader

from typing import Dict, Tuple, List, Iterable


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

    def line(self) -> Iterable[Tuple[int, int]]:
        x_range = list(self._range(self.c1[0], self.c2[0]))
        y_range = list(self._range(self.c1[1], self.c2[1]))
        for i in range(max(len(x_range), len(y_range))):
            yield x_range[i] if i < len(x_range) else x_range[0], \
                  y_range[i] if i < len(y_range) else y_range[0]

    # Alternate form?  More lines of code, but fewer if-checks since they're not looped
    #
    # def line(self) -> Iterable[Tuple[int, int]]:
    #     x_range = list(self._range(self.c1[0], self.c2[0]))
    #     y_range = list(self._range(self.c1[1], self.c2[1]))
    #     if len(x_range) < len(y_range):
    #         x_range = x_range * len(y_range)
    #     elif len(x_range) > len(y_range):
    #         y_range = y_range * len(x_range)
    #     return zip(x_range, y_range)

    @staticmethod
    def _range(val1: int, val2: int) -> Iterable[int]:
        if val1 <= val2:
            return range(val1, val2 + 1)
        else:
            return range(val1, val2 - 1, -1)

    @staticmethod
    def parse(line: str) -> Line:
        return Line(*(tuple(int(x) for x in coord.strip().split(",")) for coord in line.split("->")))


#


if __name__ == '__main__':
    main()
