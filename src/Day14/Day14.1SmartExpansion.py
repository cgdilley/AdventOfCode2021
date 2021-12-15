from __future__ import annotations

from Utility import InputLoader

from Day14.Day14Shared import Instruction

from typing import Dict

STEPS = 10


#

# THIS IS AN UNFINISHED IDEA

#

#

# THIS IS AN UNFINISHED IDEA

#

#

# THIS IS AN UNFINISHED IDEA

#

#

# THIS IS AN UNFINISHED IDEA

#


def main():
    with InputLoader(day=14, sample=True) as reader:
        sequence = next(reader)
        reader.skip_line()
        instructions: Dict[str, Instruction] = {x.pair: x for x in (Instruction.parse(line) for line in reader)}

    # loops = get_loops(instructions)

    # count = expand_smart(sequence, STEPS, instructions, loops)

    raw = expand_raw(sequence, STEPS, instructions)
    print(raw)
    print(count_chars(raw))

    sortable = [(num, c) for c, num in count.items()]
    max_num, max_char = max(sortable)
    min_num, min_char = min(sortable)
    print(f"MAX CHAR ({max_char}) = {max_num}")
    print(f"MIN CHAR ({min_char}) = {min_num}")
    print(f"RESULT = {max_num - min_num}")


def get_loops(instructions: Dict[str, Instruction]) -> Dict[str, Loop]:
    loops: Dict[str, Loop] = dict()
    for inst in instructions.values():
        loop = Loop.find(inst.pair, instructions)
        loops[loop.seed] = loop

    return loops


def expand_raw(sequence: str, iterations: int, instructions: Dict[str, Instruction]) -> str:
    for _ in range(iterations):
        new_sequence = ""
        for i in range(len(sequence) - 1):
            pair = sequence[i:i + 2]
            if pair in instructions:
                new_sequence += instructions[pair].result[:-1]
            else:
                new_sequence += pair[0]
        sequence = new_sequence + sequence[-1]
        print(sequence)
    return sequence


def count_chars(s: str) -> Dict[str, int]:
    count: Dict[str, int] = dict()
    for c in s:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
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


def expand_smart(sequence: str, iterations: int, instructions: Dict[str, Instruction],
                 loops: Dict[str, Loop]) -> Dict[str, int]:
    if iterations <= 0:
        return count_chars(sequence)
    return add_counts(add_counts(*(_expand_pair_smart(sequence[i:i + 2], iterations, instructions, loops)
                                   for i in range(len(sequence) - 1))),
                      {sequence[-1]: 1})


def _expand_pair_smart(pair: str, iterations: int, instructions: Dict[str, Instruction],
                       loops: Dict[str, Loop]) -> Dict[str, int]:
    if pair in loops:
        repeats = int(iterations / loops[pair].length)
        remaining = iterations % loops[pair].length
        count = loops[pair].scale_counts(2**repeats)
        expanded = expand_raw(pair, remaining, instructions)
        final = add_counts(count,
                           scale_counts(count_chars(expanded[1:-1]), 2**repeats))
        return final
    else:
        expanded = expand_raw(pair, 1, instructions)
        return add_counts(expand_smart(expanded, iterations - 1, instructions, loops),
                          {expanded[-1]: -1})


#


class Loop:

    def __init__(self, seed: str, length: int, counts: Dict[str, int]):
        self.seed = seed
        self.length = length
        self.counts = counts

    def __len__(self) -> int:
        return self.length

    def __eq__(self, other) -> bool:
        return other.seed == self.seed

    def __hash__(self) -> int:
        return hash(self.seed)

    def __str__(self) -> str:
        return f"{self.seed} ({self.length}) --- {self.counts}"

    def __repr__(self) -> str:
        return str(self)

    def scale_counts(self, factor: int):
        return add_counts(scale_counts({c: num if c != self.seed[0] else num - 1
                                        for c, num in self.counts.items()},
                                       factor),
                          {self.seed[0]: 1})

    @staticmethod
    def find(start: str, instructions: Dict[str, Instruction]) -> Loop:
        seen = {start: 0}
        result = start
        for i in range(1, 101):
            result = instructions[result].result[:-1]
            if result in seen:
                length = i - seen[result]
                return Loop(result, length, count_chars(expand_raw(result, length, instructions)[:-1]))
            seen[result] = i


#


#


if __name__ == '__main__':
    main()
