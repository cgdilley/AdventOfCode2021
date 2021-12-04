from __future__ import annotations

from typing import List, Tuple, Dict, Iterable, Iterator


class BingoBoard:

    def __init__(self, values: List[List[int]]):
        self.values = values
        self.height = len(values)
        self.width = len(values[0]) if self.height > 0 else 0
        self._selected: Dict[Tuple[int, int], bool] = dict()
        self._value_map: Dict[int, Tuple[int, int]] = \
            {value: (y, x) for y, row in enumerate(self.values) for x, value in enumerate(row)}

    def test_winning_move(self, position: Tuple[int, int]) -> bool:
        return all(self.is_selected((position[0], col)) for col in range(self.width)) or \
               all(self.is_selected((row, position[1])) for row in range(self.height))

    def is_selected(self, position: Tuple[int, int]) -> bool:
        return position in self._selected and self._selected[position]

    def select(self, value: int) -> bool:
        if value in self._value_map:
            self._selected[self._value_map[value]] = True
            return self.test_winning_move(self._value_map[value])
        return False

    def sum_unselected(self):
        s = 0
        for pos, value in self.iterate():
            if not self.is_selected(pos):
                s += value
        return s

    def iterate(self) -> Iterable[Tuple[Tuple[int, int], int]]:
        for y, row in enumerate(self.values):
            for x, col in enumerate(row):
                yield (y, x), col

    def render(self) -> str:
        def _draw(y, x) -> str:
            val = str(self.values[y][x]).rjust(2, " ")
            return f"({val})" if self.is_selected((y, x)) else f" {val} "
        return "\n".join(" ".join(_draw(y, x) for x, col in enumerate(row)) for y, row in enumerate(self.values))

    def __str__(self) -> str:
        return " || ".join(" ".join(str(col).rjust(2, " ") for col in row) for row in self.values)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def parse_board(data: Iterable[str]) -> BingoBoard:
        values: List[List[int]] = []
        for line in data:
            if not line:
                break
            row = [int(col) for col in line.split(" ") if col]
            values.append(row)
        return BingoBoard(values)


#


def load_instructions(data: Iterator[str]) -> List[int]:
    line = next(data)
    return [int(x) for x in line.split(",") if x]
