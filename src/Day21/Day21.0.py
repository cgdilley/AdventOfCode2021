
from Utility import InputLoader

from Day21.Day21Shared import Player, Die, Dirac

from typing import List, Optional, Tuple, Dict, Set, Iterable


def main():
    with InputLoader(day=21) as reader:
        players = [Player(int(line[-2:].strip())) for line in reader]

    game = Dirac(*players)
    die = DeterministicDie(100)

    while not game.is_over():
        game.take_turn(die)

    loser = min(game.players)
    print(f"RESULT = {loser.score * die.rolls}")

#


class DeterministicDie(Die):

    def __init__(self, size: int):
        self.size = size
        self.next_value = 1
        self.rolls = 0

    def roll(self) -> int:
        val = self.next_value
        self.next_value = (self.next_value % self.size) + 1
        self.rolls += 1
        return val


#


#


if __name__ == '__main__':
    main()
