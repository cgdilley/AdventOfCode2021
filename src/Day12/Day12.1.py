
from Utility import InputLoader
from Day12.Day12Shared import Cave, CaveSystem

from typing import Iterable, List, Dict, Tuple, Optional, Set


ALLOWED_SMALL_REPEATS = 1


def main():
    with InputLoader(day=12) as reader:
        system = CaveSystem.parse(reader)

    paths = set(find_all_paths(system))
    print(f"TOTAL PATHS = {len(paths)}")
    # for path in sorted(paths):
    #     print(",".join(c.title for c in path))

#


def find_all_paths(system: CaveSystem) -> Iterable[Tuple[Cave]]:
    yield from _find_paths_from(system["start"], (system["start"],), 0)


def _find_paths_from(cave: Cave, path_so_far: Tuple[Cave, ...], small_repeats: int = 0) -> Iterable[Tuple[Cave, ...]]:
    if cave.is_end():
        yield path_so_far
    else:
        for connection in cave.all_paths():
            if connection.is_start():
                continue
            elif connection.is_small() and connection in path_so_far:
                if small_repeats >= ALLOWED_SMALL_REPEATS:
                    continue
                yield from _find_paths_from(connection, path_so_far + (connection,), small_repeats + 1)
            else:
                yield from _find_paths_from(connection, path_so_far + (connection,), small_repeats)


#


#


if __name__ == '__main__':
    main()
