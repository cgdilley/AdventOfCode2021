from __future__ import annotations

from typing import List, Tuple, Set, Iterable


class Fold:

    def __init__(self, direction: str, position: int):
        self.direction = direction
        self.position = position

    def __str__(self) -> str:
        return f"{self.direction}={self.position}"

    def __repr__(self) -> str:
        return str(self)

    def perform_fold(self, dots: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        if self.direction == "y":
            return {(x, y) if y < self.position else (x, (2 * self.position) - y)
                    for x, y in dots}
        elif self.direction == "x":
            return {(x, y) if x < self.position else ((2 * self.position) - x, y)
                    for x, y in dots}
        raise Exception(f"Invalid fold direction '{self.direction}'.")

    @staticmethod
    def parse(line: str) -> Fold:
        direction, position = line[11:].split("=")
        return Fold(direction, int(position))
