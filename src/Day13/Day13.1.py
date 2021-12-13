
from Utility import InputLoader
from Day13.Day13Shared import Fold

from typing import List, Tuple, Dict, Iterable, Optional, Set


def main():
    dots, folds = load_input()
    print(f"NUMBER OF DOTS BEFORE FOLDS: {len(dots)}")

    # render(dots)

    for fold in folds:
        dots = fold.perform_fold(dots)
        # render(dots)

    render(dots)
    print(f"NUMBER OF DOTS AFTER ALL FOLDS: {len(dots)}")


#


def load_input() -> Tuple[Set[Tuple[int, int]], List[Fold]]:
    with InputLoader(day=13) as reader:
        dots: Set[Tuple[int, int]] = set()
        for line in reader:
            if not line:
                break
            x, y = line.split(",")
            dots.add((int(x), int(y)))

        folds: List[Fold] = [Fold.parse(line) for line in reader]
    return dots, folds


def render(dots: Set[Tuple[int, int]]):
    # Multiple iteration isn't good but I'm lazy
    min_x = min(d[0] for d in dots)
    min_y = min(d[1] for d in dots)
    max_x = max(d[0] for d in dots)
    max_y = max(d[1] for d in dots)
    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x+1):
            line += "##" if (x, y) in dots else ".."
        print(line)
    print()


#


#


if __name__ == '__main__':
    main()
