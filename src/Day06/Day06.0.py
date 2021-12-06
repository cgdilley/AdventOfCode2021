from Utility import InputLoader

from typing import Dict, Tuple
import math

with InputLoader(day=6) as reader:
    fish = [int(x) for line in reader for x in line.split(",")]

duration = 80
spawn_rate = 7
new_delay = 2


def naive():
    for _ in range(duration):
        new = 0
        for i, f in enumerate(fish):
            if f == 0:
                fish[i] = spawn_rate - 1
                new += 1
            else:
                fish[i] = f - 1
        fish.extend([spawn_rate + new_delay - 1] * new)

    print(f"NUMBER OF FISH: {len(fish)}")


def recursion():

    cache: Dict[Tuple[int, int], int] = dict()

    def extra(cycle: int, span: int) -> int:
        if (cycle, span) in cache:
            return cache[(cycle, span)]

        adjusted_span = span - cycle - 1
        spawned = math.floor(adjusted_span / spawn_rate) + 1
        if spawned <= 0:
            total = 0
        else:
            total = sum(1 + extra(cycle=spawn_rate + new_delay - 1,
                                  span=(adjusted_span - (spawn_rate * i)))
                        for i in range(spawned))
        cache[(cycle, span)] = total
        return total

    total_fish = sum(extra(f, duration) + 1 for f in fish)

    print(f"NUMBER OF FISH: {total_fish}")


def equation():
    pass


#


if __name__ == '__main__':
    recursion()
