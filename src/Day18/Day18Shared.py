from __future__ import annotations

from typing import Tuple, Union, Iterable, Iterator, Optional
import math

EXPLOSION_DEPTH = 4


class SnailPair:

    def __init__(self, left: Union[int, SnailPair], right: Union[int, SnailPair]):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other) -> SnailPair:
        if not isinstance(other, SnailPair):
            raise ValueError("Can only add SnailPairs to SnailPairs.")
        return SnailPair(self, other).copy().reduce()

    def reduce(self) -> SnailPair:
        while True:
            aftermath = self.do_explosions(0)
            if aftermath is None:
                if not self.do_splits():
                    break
        return self

    def add_to_left(self, val: int):
        if isinstance(self.left, SnailPair):
            self.left.add_to_left(val)
        else:
            self.left += val

    def add_to_right(self, val: int):
        if isinstance(self.right, SnailPair):
            self.right.add_to_right(val)
        else:
            self.right += val

    def do_explosions(self, depth: int) -> Optional[Tuple[int, int]]:
        """
        Triggers the left-most explosion, and returns the remnants of that explosion.
        If returning None, then no explosion occurred.

        This is called recursively, and any remnants from a nested node's explosion are
        passed up to it's parent, which will add those remnants into the appropriate
        neighbor values, and turn that exploded pair into a 0.

        :param depth: The current depth, for triggering explosions
        :return: Remnants remaining at this depth after any nested node that has exploded,
        or None if no explosion has occurred.
        """
        if depth >= EXPLOSION_DEPTH:
            return self.left, self.right
        if isinstance(self.left, SnailPair):
            values = self.left.do_explosions(depth + 1)
            if values is not None:
                if depth >= EXPLOSION_DEPTH - 1:
                    self.left = 0
                if isinstance(self.right, SnailPair):
                    self.right.add_to_left(values[1])
                else:
                    self.right += values[1]
                return values[0], 0
        if isinstance(self.right, SnailPair):
            values = self.right.do_explosions(depth + 1)
            if values is not None:
                if depth >= EXPLOSION_DEPTH - 1:
                    self.right = 0
                if isinstance(self.left, SnailPair):
                    self.left.add_to_right(values[0])
                else:
                    self.left += values[0]
                return 0, values[1]
        return None

    def do_splits(self) -> bool:
        """
        Splits the left-most value that requires splitting.

        :return: Returns True if a splitting occurred, False otherwise.
        """
        if isinstance(self.left, SnailPair):
            if self.left.do_splits():
                return True
        elif self.left > 9:
            self.left = SnailPair(math.floor(self.left/2), math.ceil(self.left/2))
            return True
        if isinstance(self.right, SnailPair):
            if self.right.do_splits():
                return True
        elif self.right > 9:
            self.right = SnailPair(math.floor(self.right/2), math.ceil(self.right/2))
            return True
        return False

    def magnitude(self) -> int:
        left_mag = 3 * (self.left.magnitude() if isinstance(self.left, SnailPair) else self.left)
        right_mag = 2 * (self.right.magnitude() if isinstance(self.right, SnailPair) else self.right)
        return left_mag + right_mag

    def copy(self) -> SnailPair:
        return SnailPair(self.left.copy() if isinstance(self.left, SnailPair) else self.left,
                         self.right.copy() if isinstance(self.right, SnailPair) else self.right)

    @classmethod
    def parse(cls, line: str) -> SnailPair:
        return cls._parse(iter(line[1:]))

    @classmethod
    def _parse(cls, line: Iterator[str]) -> SnailPair:
        values = []
        for char in line:
            if char == "[":
                values.append(cls._parse(line))
            elif char == ",":
                continue
            elif char == "]":
                if len(values) != 2:
                    raise Exception("Invalid pair")
                return SnailPair(*values)
            else:
                values.append(int(char))
        raise Exception("Parsing error.")


