from __future__ import annotations

from Utility import InputLoader

from typing import List, Dict
import functools


SEGMENTS = "abcdefg"
SEGMENT_MAP = {s: 1 << len(SEGMENTS)-i-1 for i, s in enumerate(SEGMENTS)}
ONES = (1 << len(SEGMENTS)) - 1


def main():
    with InputLoader(day=8) as reader:
        total = sum(process_reading(Reading.parse(line)) for line in reader)
    print(f"TOTAL = {total}")


def process_reading(reading: Reading) -> int:

    possibilities: Dict[int, int] = {SEGMENT_MAP[s]: ONES for s in SEGMENTS}

    for length in range(len(SEGMENTS) + 1):
        if len(LENGTH_GROUPING[length]) == 0:
            continue

        segments_in_common_in_input = functools.reduce(lambda a, s: a & s,
                                                       [s for s in reading.samples if count_set(s) == length],
                                                       ONES)

        segments_in_common = SEGMENTS_IN_COMMON[length]
        for i in range(len(SEGMENTS)):
            segment = 1 << i
            if segment & segments_in_common_in_input != 0:
                possibilities[segment] &= segments_in_common
            else:
                possibilities[segment] &= ~segments_in_common

    # Is it possible to do this without an if statement embedded?
    converted = [functools.reduce(lambda a, s: a | (possibilities[s] if s & output != 0 else 0),
                                  possibilities.keys(),
                                  0)
                 for output in reading.output]
    result_str = "".join(str(REVERSE_DIGIT_PATTERNS[c]) for c in converted)
    return int(result_str)


def segments_to_int(segments: str) -> int:
    return functools.reduce(lambda i, s: i | SEGMENT_MAP[s], segments, 0)


def count_set(val: int) -> int:
    return bin(val).count("1")


DIGIT_PATTERNS = {
    0: segments_to_int("abcefg"),
    1: segments_to_int("cf"),
    2: segments_to_int("acdeg"),
    3: segments_to_int("acdfg"),
    4: segments_to_int("bcdf"),
    5: segments_to_int("abdfg"),
    6: segments_to_int("abdefg"),
    7: segments_to_int("acf"),
    8: segments_to_int("abcdefg"),
    9: segments_to_int("abcdfg")
}
REVERSE_DIGIT_PATTERNS = {v: k for k, v in DIGIT_PATTERNS.items()}

LENGTH_GROUPING: Dict[int, List[int]] = {i: [] for i in range(len(SEGMENTS) + 1)}
for digit, seg in DIGIT_PATTERNS.items():
    LENGTH_GROUPING[count_set(seg)].append(digit)
SEGMENTS_IN_COMMON = {
    length: functools.reduce(lambda a, s: a & s,
                             (DIGIT_PATTERNS[d] for d in LENGTH_GROUPING[length]),
                             ONES)
    for length in range(2, 8) if len(LENGTH_GROUPING[length]) > 0
}


class Reading:

    def __init__(self, samples: List[int], output: List[int]):
        if len(samples) != 10 or len(output) != 4:
            raise Exception("Invalid reading.")
        self.samples = samples
        self.output = output

    @staticmethod
    def parse(line: str) -> Reading:
        sample_str, output_str = line.split(" | ")
        return Reading([segments_to_int(s) for s in sample_str.split()],
                       [segments_to_int(s) for s in output_str.split()])


if __name__ == '__main__':
    main()
