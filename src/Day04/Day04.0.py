from __future__ import annotations

from Utility import InputLoader
from Day04.Day04Shared import load_instructions, BingoBoard

from typing import List, Tuple, Dict, Iterable, Iterator


#


def main():
    with InputLoader(day=4) as reader:
        instructions = load_instructions(reader)
        reader.skip_line()

        boards: List[BingoBoard] = []
        while reader.is_open():
            boards.append(BingoBoard.parse_board(reader))

    #

    for instruction in instructions:
        winners = [board for board in boards if board.select(instruction)]
        if len(winners) > 0:
            for winner in winners:
                print(f"WINNER: {winner}")
                print(f"SUM OF UNMARKED: {winner.sum_unselected()}")
                print(f"LAST INSTRUCTION: {instruction}")
                print(f"MULTIPLIED: {winner.sum_unselected() * instruction}")
                print("\n" + winner.render())
            break


#


#


if __name__ == '__main__':
    main()
