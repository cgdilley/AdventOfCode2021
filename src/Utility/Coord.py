from __future__ import annotations

from typing import Tuple, Set, Dict, Optional, TypeVar, Generic, Union, Hashable, Iterable, Iterator, \
    SupportsAbs


class Coord(Iterable[int], Hashable):

    def __init__(self, coord: Tuple[int, int]):
        self.coord = coord

    @staticmethod
    def of(v1: int, v2: int) -> Coord:
        return Coord((v1, v2))

    @property
    def r(self) -> int:
        return self.coord[0]

    @property
    def c(self) -> int:
        return self.coord[1]

    @property
    def x(self) -> int:
        return self.coord[0]

    @property
    def y(self) -> int:
        return self.coord[1]

    def __iter__(self) -> Iterator[int]:
        return iter(self.coord)

    def __hash__(self) -> int:
        return hash(self.coord)

    def __eq__(self, other) -> bool:
        return isinstance(other, Coord) and other.coord == self.coord

    def __lt__(self, other) -> bool:
        return isinstance(other, Coord) and self.coord < other.coord

    def __gt__(self, other) -> bool:
        return isinstance(other, Coord) and self.coord > other.coord

    def __add__(self, other: Coord) -> Coord:
        return Coord.of(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coord) -> Coord:
        return Coord.of(self.x - other.x, self.y - other.y)

    def __abs__(self) -> Coord:
        return Coord.of(abs(self.x), abs(self.y))

    def __str__(self) -> str:
        return str(self.coord)

    def __repr__(self) -> str:
        return str(self)

    def distance(self, other: Coord) -> int:
        return sum(abs(self - other))


