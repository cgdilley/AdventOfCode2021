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
        remaining = [board for board in boards if not board.select(instruction)]
        if len(remaining) == 0 and len(boards) == 1:
            loser = boards[0]
            print(f"LOSER: {loser}")
            print(f"SUM OF UNMARKED: {loser.sum_unselected()}")
            print(f"LAST INSTRUCTION: {instruction}")
            print(f"MULTIPLIED: {loser.sum_unselected() * instruction}")
            print("\n" + loser.render())
            break
        boards = remaining


#


#


if __name__ == '__main__':
    main()
