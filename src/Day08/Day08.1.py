from Utility import InputLoader
from Day08.Day08Shared import Reading, DIGIT_PATTERNS, LENGTH_GROUPING, UNIQUE_LENGTHS, REVERSE_DIGIT_PATTERNS

from typing import Dict, List, Set


with InputLoader(day=8) as reader:
    readings = (Reading.parse(line) for line in reader)

SEGMENTS = "abcdefg"


def intersections():
    """
    The idea behind this solution is that you can solve the connections by identifying the segments that are used
    by all numbers with a certain number of total segments, and then identifying the segments that are used in all
    the samples in the reading for a certain number of total segments.  This narrows the possibilities of which
    segments can translate to which others.  If you do this for all possible segment totals, you'll eventually narrow
    down each segment to just one possibility, which is the correct answer.
    """
    total = sum(process_reading(reading) for reading in readings)
    print(f"TOTAL: {total}")


#


def process_reading(reading: Reading) -> int:
    # Initial possibilities:  Any segment can translate to any other
    possibilities: Dict[str, Set[str]] = {s: set(SEGMENTS) for s in SEGMENTS}

    # length = 7 doesn't matter, doesn't help narrow anything down
    for length in range(2, 7):
        if len(LENGTH_GROUPING[length]) == 0:
            continue

        segments_in_common_in_input = \
            _intersect_segments(*(sample for sample in reading.samples if len(sample) == length))

        # Compare this set of segments that are in common amongst the samples of this length against the
        # set of segments that are in common among valid digits of this length.  These segments from the samples
        # must in some way map to the segments from the valid digits, and cannot map to anything else.
        # Therefore, for segments in common, you can intersect the mapped characters against the currently
        # remaining possibilities for those segments, narrowing down the selection.  In addition,
        # you can remove these as possibilities for all other segments.
        #
        # For example, the digit 1 uses segments "cf".  If you see a sample "ab", you know
        # a and b must map to either c or f (and nothing else), and nothing else can map to c or f.
        #
        # For another example, 2, 3, and 5 all have 5 segments (acdeg, acdfg, and abdfg, respectively).  They all
        # have the segments a, d, and g in common.  That means among all the samples of length 5, there will be exactly
        # 3 segments that are shared as well, and these 3 segments must map to a, d, or g, and nothing else can map
        # to a, d, or g.

        segments_in_common = SEGMENTS_IN_COMMON[length]
        for segment in SEGMENTS:
            if segment in segments_in_common_in_input:
                possibilities[segment] = possibilities[segment].intersection(segments_in_common)
            else:
                possibilities[segment] = possibilities[segment].difference(segments_in_common)

    if not all(len(p) == 1 for p in possibilities.values()):
        raise Exception("COULD NOT SOLVE")

    final = {i: "".join(o) for i, o in possibilities.items()}

    converted = ["".join(sorted(final[s] for s in output)) for output in reading.output]
    result_str = "".join(str(REVERSE_DIGIT_PATTERNS[c]) for c in converted)
    return int(result_str)


def _intersect_segments(*patterns: str) -> Set[str]:
    """
    Finds the set of characters that are in common in all of the given input patterns.
    """
    return set(SEGMENTS).intersection(*(set(pattern) for pattern in patterns))


SEGMENTS_IN_COMMON = {
    length: _intersect_segments(*(DIGIT_PATTERNS[d] for d in LENGTH_GROUPING[length]))
    for length in range(2, 8) if len(LENGTH_GROUPING[length]) > 0
}


#


#


if __name__ == '__main__':
    intersections()
