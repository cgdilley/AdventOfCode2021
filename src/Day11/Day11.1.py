
from Utility import InputLoader

from typing import Iterable, Tuple, Set, List


with InputLoader(day=11) as reader:
    octopuses = [[int(o) for o in line] for line in reader]


def simulate():
    total = sum(len(line) for line in octopuses)

    # render(set())

    # This "step_amount" thing doesn't really help much, shaves off <10% of iterations, and the extra
    # overhead to manage this might just make it slower overall.  I think it's fun though
    step = 0
    step_amount = 1
    while True:
        step += step_amount
        maximum = increase_energy_for_all(step_amount)
        step_amount = 10 - min(maximum, 9)
        flashed = trigger_all_flashes()
        if len(flashed) == total:
            break
        # render(flashed)
    print(f"STEP = {step}")


def increase_energy_for_all(amount: int) -> int:
    maximum = 0
    for row in range(len(octopuses)):
        for col in range(len(octopuses[row])):
            octopuses[row][col] += amount
            if octopuses[row][col] > maximum:
                maximum = octopuses[row][col]
    return maximum


def trigger_all_flashes() -> Set[Tuple[int, int]]:
    flashed: Set[Tuple[int, int]] = set()
    for row in range(len(octopuses)):
        for col in range(len(octopuses[row])):
            if octopuses[row][col] > 9:
                trigger_flash(row, col, flashed)
    for row, col in flashed:
        octopuses[row][col] = 0
    return flashed


def trigger_flash(row: int, col: int, flashed: Set[Tuple[int, int]]):
    if (row, col) in flashed:
        return
    flashed.add((row, col))
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if not 0 <= row + dy < len(octopuses) or not 0 <= col + dx < len(octopuses[row + dy]):
                continue
            octopuses[row + dy][col + dx] += 1
            if octopuses[row + dy][col + dx] > 9:
                trigger_flash(row + dy, col + dx, flashed)


def render(flashed: Set[Tuple[int, int]]):
    print("\n".join("".join(str(o) if (row, col) not in flashed else "*"
                            for col, o in enumerate(line)) for row, line in enumerate(octopuses)))
    print()


if __name__ == '__main__':
    simulate()
