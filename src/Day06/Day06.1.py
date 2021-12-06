from Utility import InputLoader

from typing import Dict, Tuple
import math

with InputLoader(day=6) as reader:
    fish = [int(x) for line in reader for x in line.split(",")]

duration = 256
spawn_rate = 7
new_delay = 2


# def naive():
#     for _ in range(duration):
#         new = 0
#         for i, f in enumerate(fish):
#             if f == 0:
#                 fish[i] = spawn_rate - 1
#                 new += 1
#             else:
#                 fish[i] = f - 1
#         fish.extend([spawn_rate + new_delay - 1] * new)
#
#     print(f"NUMBER OF FISH: {len(fish)}")


# def recursion():
#
#     cache: Dict[Tuple[int, int], int] = dict()
#
#     def extra(cycle: int, span: int) -> int:
#         if (cycle, span) in cache:
#             return cache[(cycle, span)]
#
#         adjusted_span = span - cycle - 1
#         spawned = math.floor(adjusted_span / spawn_rate) + 1
#         if spawned <= 0:
#             total = 0
#         else:
#             # For each spawned fish, add 1 to the total, plus any fish that would descend from that fish
#             # in the remaining time
#             total = sum(1 + extra(cycle=spawn_rate + new_delay - 1,
#                                   span=(adjusted_span - (spawn_rate * i)))
#                         for i in range(spawned))
#         cache[(cycle, span)] = total
#         return total
#
#     total_fish = sum(extra(f, duration) + 1 for f in fish)
#
#     print(f"NUMBER OF FISH: {total_fish}")


def recursion_improved():
    """
    The idea of this solution is to find for each fish the total number of fish that will end up in that fish's
    lineage, given the remaining time.  This is always 1 (the fish itself) plus the number of fish in each of
    the children's lineages (invoking some recursion).  The cache is used to avoid calculating the same
    value twice, short-circuiting the recursion.
    """
    cache: Dict[int, int] = dict()

    def descendants(span: int) -> int:
        if span in cache:
            return cache[span]
        spawned = math.floor(span / spawn_rate) + 1
        if spawned <= 0:
            total = 0
        else:
            # For each spawned fish, add 1 to the total, plus any fish that would descend from that fish
            # in the remaining time
            total = sum(1 + descendants(span - (spawn_rate + new_delay) - (spawn_rate * i))
                        for i in range(spawned))
        cache[span] = total
        return total

    values = {i: 1 + descendants(duration - i - 1) for i in range(spawn_rate)}
    total_fish = sum(values[f] for f in fish)

    print(f"NUMBER OF FISH: {total_fish}")


def martje():
    """
    This solution is courtesy of Martje, who did it in a way smarter way than I did (above).
    This solution iterates through each time step, and adjusts how many fish have how many days remaining
    until their next spawn.  For each time step, the number of days remaining until spawning is shifted over by 1,
    discarding all fish that spawn on that time step.  New fish (equal in number to the amount of
    discarded fish) are added that will spawn 7 and 9 days later.
    """

    extended_spawn_rate = spawn_rate + new_delay

    fish_table = [0] * extended_spawn_rate
    for f in fish:
        fish_table[f] += 1

    for i in range(duration):
        ready = fish_table.pop(0)

        fish_table[spawn_rate - 1] += ready
        fish_table.append(ready)

    total_fish = sum(fish_table)
    print(f"NUMBER OF FISH: {total_fish}")


def equation():
    pass


#


if __name__ == '__main__':
    martje()
