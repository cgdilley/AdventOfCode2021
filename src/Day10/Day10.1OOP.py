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
        analyses = [Analysis.analyze(line) for line in reader]

    corruption_score = sum(a.score for a in analyses if a.result == Analysis.Result.CORRUPTED)
    completion_scores = [a.score for a in analyses if a.result == Analysis.Result.INCOMPLETE]
    completion_score = statistics.median(completion_scores)
    print(f"CORRUPTION SCORE = {corruption_score}")
    print(f"COMPLETION SCORE = {completion_score}")


#


class Analysis:

    class Result(Enum):
        CORRUPTED = 0
        INCOMPLETE = 1
        VALID = 2

    def __init__(self, corrupter: Optional[str], completion: Optional[str]):
        self.corrupter = corrupter
        self.completion = completion

    @property
    def result(self) -> Analysis.Result:
        if self.corrupter is not None:
            return Analysis.Result.CORRUPTED
        elif self.completion:
            return Analysis.Result.INCOMPLETE
        return Analysis.Result.VALID

    @property
    def score(self) -> int:
        if self.result == Analysis.Result.CORRUPTED:
            return CORRUPTION_SCORES[self.corrupter]
        elif self.result == Analysis.Result.INCOMPLETE:
            score = 0
            for char in self.completion:
                score *= 5
                score += COMPLETION_SCORES[char]
            return score
        else:
            return 0

    @staticmethod
    def analyze(line: str) -> Analysis:
        stack = []
        for char in line:
            if char in OPENERS:
                stack.append(char)
            else:
                if len(stack) > 0 and stack[-1] == REVERSE_PAIRINGS[char]:
                    stack.pop(-1)
                else:
                    return Analysis(char, None)
        return Analysis(None, "".join(PAIRINGS[c] for c in reversed(stack)))


#


if __name__ == '__main__':
    main()
