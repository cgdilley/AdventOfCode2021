
from Utility import InputLoader

from typing import Iterable, Optional, List, Dict, Tuple, Set


#


PAIRINGS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
REVERSE_PAIRINGS = {v: k for k, v in PAIRINGS.items()}
OPENERS = {c for c in PAIRINGS.keys()}
CLOSERS = {c for c in PAIRINGS.values()}

SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def main():
    with InputLoader(day=10) as reader:
        error_score = sum(SCORES[c] for c in (find_corrupted_character(line) for line in reader) if c is not None)
        print(f"ERROR SCORE = {error_score}")


def find_corrupted_character(line: str) -> Optional[str]:
    stack = []
    for char in line:
        if char in OPENERS:
            stack.append(char)
        else:
            if len(stack) > 0 and stack[-1] == REVERSE_PAIRINGS[char]:
                stack.pop(-1)
            else:
                return char
    return None


#


if __name__ == '__main__':
    main()
