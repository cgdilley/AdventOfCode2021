from __future__ import annotations

from enum import Enum
from typing import Tuple


class MovementCommand:

    class Direction(Enum):
        FORWARD = "forward"
        DOWN = "down"
        UP = "up"

    def __init__(self, direction: MovementCommand.Direction, amount: int):
        self.direction = direction
        self.amount = amount

    def adjust_direct(self, start: Tuple[int, int]) -> Tuple[int, int]:
        """
        For Day2.0.
        """
        if self.direction == MovementCommand.Direction.FORWARD:
            return start[0] + self.amount, start[1]
        elif self.direction == MovementCommand.Direction.DOWN:
            return start[0], start[1] + self.amount
        elif self.direction == MovementCommand.Direction.UP:
            return start[0], start[1] - self.amount
        else:
            return start

    def adjust(self, start: Tuple[int, int], aim: int) -> Tuple[Tuple[int, int], int]:
        """
        For Day2.1.
        """
        if self.direction == MovementCommand.Direction.UP:
            return start, aim - self.amount
        elif self.direction == MovementCommand.Direction.DOWN:
            return start, aim + self.amount
        elif self.direction == MovementCommand.Direction.FORWARD:
            return (start[0] + self.amount, start[1] + (self.amount * aim)), aim
        else:
            return start, aim

    @staticmethod
    def parse(command: str) -> MovementCommand:
        split = command.split(" ")
        return MovementCommand(direction=MovementCommand.Direction(split[0]),
                               amount=int(split[1]))
