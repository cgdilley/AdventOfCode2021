from __future__ import annotations

from Utility import InputLoader

from typing import Iterable, Optional, List, Dict, Tuple, Set
from enum import Enum
import statistics


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

CORRUPTION_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
COMPLETION_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def main():
    with InputLoader(day=10) as reader:
        scores = [completion_score(c) for c in (find_completion_string(line) for line in reader)
                  if c is not None]
    middle = statistics.median(scores)
    print(f"COMPLETION SCORE = {middle}")


def find_completion_string(line: str) -> Optional[str]:
    stack = []
    for char in line:
        if char in OPENERS:
            stack.append(char)
        else:
            if len(stack) > 0 and stack[-1] == REVERSE_PAIRINGS[char]:
                stack.pop(-1)
            else:
                return None
    return "".join(PAIRINGS[c] for c in reversed(stack))


def completion_score(ending: str) -> int:
    score = 0
    for char in ending:
        score *= 5
        score += COMPLETION_SCORES[char]
    return score


#


if __name__ == '__main__':
    main()
