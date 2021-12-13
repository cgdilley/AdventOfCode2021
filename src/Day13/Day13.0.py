
from Utility import InputLoader
from Day13.Day13Shared import Fold

from typing import List, Tuple, Dict, Iterable, Optional, Set


def main():
    dots, folds = load_input()

    new_dots = set(folds[0].perform_fold(dots))

    print(f"NUMBER OF DOTS BEFORE FOLD: {len(dots)}")
    print(f"NUMBER OF DOTS AFTER FIRST FOLD: {len(new_dots)}")


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


#


#


if __name__ == '__main__':
    main()
