
from Utility import InputLoader

from Day14.Day14Shared import Instruction

from typing import Dict


STEPS = 40


def main():
    with InputLoader(day=14) as reader:
        sequence = next(reader)
        reader.skip_line()
        instructions: Dict[str, Instruction] = {x.pair: x for x in (Instruction.parse(line) for line in reader)}

    pair_count: Dict[str, int] = count_pairs(sequence)

    for _ in range(STEPS):
        new_pair_count: Dict[str, int] = dict()
        for pair, count in pair_count.items():
            expand = instructions[pair].result
            new_pair_count = add_counts(new_pair_count,
                                        scale_counts(count_pairs(expand), count))
        pair_count = new_pair_count

    char_count = add_counts(get_char_count_from_pair_count(pair_count),
                            {sequence[-1]: 1})
    sortable = [(num, c) for c, num in char_count.items()]
    max_num, max_char = max(sortable)
    min_num, min_char = min(sortable)
    print(f"MAX CHAR ({max_char}) = {max_num}")
    print(f"MIN CHAR ({min_char}) = {min_num}")
    print(f"RESULT = {max_num - min_num}")


#


def count_pairs(s: str) -> Dict[str, int]:
    count: Dict[str, int] = dict()
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        if pair in count:
            count[pair] += 1
        else:
            count[pair] = 1
    return count


def scale_counts(counts: Dict[str, int], factor: int) -> Dict[str, int]:
    return {s: c * factor for s, c in counts.items()}


def add_counts(*counts: Dict[str, int]) -> Dict[str, int]:
    if len(counts) == 1:
        return counts[0]
    others = add_counts(*counts[1:])
    result = {k: v for k, v in counts[0].items()}
    for k, v in others.items():
        if k in result:
            result[k] += v
        else:
            result[k] = v
    return result


def get_char_count_from_pair_count(pair_count: Dict[str, int]) -> Dict[str, int]:
    char_count: Dict[str, int] = dict()
    for pair, count in pair_count.items():
        if pair[0] in char_count:
            char_count[pair[0]] += count
        else:
            char_count[pair[0]] = count
    return char_count


#


#


if __name__ == '__main__':
    main()
