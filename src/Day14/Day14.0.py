
from Utility import InputLoader

from Day14.Day14Shared import Instruction

from typing import Dict


STEPS = 10


def main():
    with InputLoader(day=14) as reader:
        sequence = next(reader)
        reader.skip_line()
        instructions: Dict[str, Instruction] = {x.pair: x for x in (Instruction.parse(line) for line in reader)}

    for _ in range(STEPS):
        new_sequence = ""
        for i in range(len(sequence) - 1):
            pair = sequence[i:i+2]
            if pair in instructions:
                new_sequence += instructions[pair].result[:-1]
            else:
                new_sequence += pair[0]
        sequence = new_sequence + sequence[-1]
        # print(sequence)

    print(sequence)
    count = count_chars(sequence)
    sortable = [(num, c) for c, num in count.items()]
    max_num, max_char = max(sortable)
    min_num, min_char = min(sortable)
    print(f"MAX CHAR ({max_char}) = {max_num}")
    print(f"MIN CHAR ({min_char}) = {min_num}")
    print(f"RESULT = {max_num - min_num}")


def count_chars(s: str) -> Dict[str, int]:
    count: Dict[str, int] = dict()
    for c in s:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
    return count


#


#


if __name__ == '__main__':
    main()
