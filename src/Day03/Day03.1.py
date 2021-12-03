
from Utility import InputLoader
from typing import List, Callable


with InputLoader(day=3) as reader:
    lines = list(reader)


def get_rating(values: List[str], length: int, criteria: Callable[[int, int], str], position: int = 0) -> str:
    if position >= length:
        return ""
    if len(values) == 1:
        return values[0][position:]
    count = {"0": 0, "1": 0}
    for value in values:
        b = value[position]
        count[b] += 1

    result = criteria(count["0"], count["1"])
    return result + get_rating([v for v in values if v[position] == result], length, criteria, position + 1)


#
# A fun alternative without using 'position'
#
# def get_rating(values: List[str], length: int, criteria: Callable[[int, int], str]) -> str:
#     if length <= 0:
#         return ""
#     if len(values) == 1:
#         return values[0]
#     count = {"0": 0, "1": 0}
#     for value in values:
#         b = value[0]
#         count[b] += 1
#
#     result = criteria(count["0"], count["1"])
#     return result + get_rating([v[1:] for v in values if v[0] == result], length - 1, criteria)


def main():
    length = len(lines[0])
    oxygen_str = get_rating(lines, length, lambda z, o: "0" if z > o else "1")
    co2_str = get_rating(lines, length, lambda z, o: "0" if z <= o else "1")

    oxygen = int(oxygen_str, 2)
    co2 = int(co2_str, 2)

    print(f"OXYGEN = {oxygen}, CO2 = {co2}")
    print(f"MULTIPLIED = {oxygen * co2}")


#


if __name__ == '__main__':
    main()
