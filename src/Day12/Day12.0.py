
from Utility import InputLoader
from Day12.Day12Shared import Cave, CaveSystem

from typing import Iterable, List, Dict, Tuple, Optional, Set


def main():
    with InputLoader(day=12) as reader:
        system = CaveSystem.parse(reader)

    paths = set(find_all_paths(system))
    print(f"TOTAL PATHS = {len(paths)}")
    for path in paths:
        print(" -- ".join(c.title for c in path))

#


def find_all_paths(system: CaveSystem) -> Iterable[Tuple[Cave]]:
    yield from _find_paths_from(system["start"], (system["start"],))


def _find_paths_from(cave: Cave, path_so_far: Tuple[Cave, ...]) -> Iterable[Tuple[Cave, ...]]:
    if cave.is_end():
        yield path_so_far
    else:
        for connection in cave.all_paths():
            if connection.is_start() or (connection.is_small() and connection in path_so_far):
                continue
            yield from _find_paths_from(connection, path_so_far + (connection,))


#


#


if __name__ == '__main__':
    main()
