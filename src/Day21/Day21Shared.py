from __future__ import annotations

from typing import List, Iterable, Set, Dict, Tuple, Optional
from abc import ABC, abstractmethod


class Dirac:

    BOARD_SIZE = 10
    SCORE_GOAL = 1000

    def __init__(self, *players: Player):
        self.players = list(players)
        self.turn = 0

    def is_over(self) -> bool:
        return any(p.score >= self.SCORE_GOAL for p in self.players)

    def winner(self) -> Optional[Player]:
        return None if not self.is_over() else max(self.players)

    def take_turn(self, die: Die):
        p = self.players[self.turn]
        roll = sum(die.roll() for _ in range(3))
        p.position += roll
        p.position = ((p.position - 1) % self.BOARD_SIZE) + 1
        p.score += p.position
        self.turn = (self.turn + 1) % len(self.players)


class Player:

    def __init__(self, position: int, score: int = 0):
        self.position = position
        self.score = score

    def __lt__(self, other: Player) -> bool:
        return self.score < other.score


class Die:

    @abstractmethod
    def roll(self) -> int: ...
