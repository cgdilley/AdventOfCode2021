
from Utility import InputLoader

from typing import Iterable, Tuple, Set, List


with InputLoader(day=11) as reader:
    octopuses = [[int(o) for o in line] for line in reader]


def simulate(steps: int):
    flashes = 0
    # render(set())
    for _ in range(steps):
        increase_energy_for_all(1)
        flashed = trigger_all_flashes()
        flashes += len(flashed)
        # render(flashed)
    print(f"TOTAL FLASHES = {flashes}")


def increase_energy_for_all(amount: int):
    for row in range(len(octopuses)):
        for col in range(len(octopuses[row])):
            octopuses[row][col] += amount


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
    simulate(steps=100)
