from __future__ import annotations

from typing import List, Dict


class Reading:

    def __init__(self, samples: List[str], output: List[str]):
        if len(samples) != 10 or len(output) != 4:
            raise Exception("Invalid reading.")
        self.samples = samples
        self.output = output

    @staticmethod
    def parse(line: str) -> Reading:
        sample_str, output_str = line.split(" | ")
        return Reading(sample_str.split(), output_str.split())


DIGIT_PATTERNS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
}

REVERSE_DIGIT_PATTERNS = {
    v: k for k, v in DIGIT_PATTERNS.items()
}

LENGTH_GROUPING: Dict[int, List[int]] = {i: [] for i in range(8)}
for digit, segments in DIGIT_PATTERNS.items():
    LENGTH_GROUPING[len(segments)].append(digit)

UNIQUE_LENGTHS = [length for length, digits in LENGTH_GROUPING.items() if len(digits) == 1]
