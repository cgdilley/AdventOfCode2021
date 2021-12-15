from __future__ import annotations

from typing import Dict, List, Iterable, Tuple, Optional, Any, Set

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Cave:

    def __init__(self, rows: Iterable[Iterable[int]]):
        self.rows = [list(r) for r in rows]

    @property
    def size(self) -> Tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def get_adjacent_positions(self, pos: Tuple[int, int]) -> Iterable[Tuple[Tuple[int, int], int]]:
        yield from (((r, c), self.rows[r][c]) for r, c in ((pos[0] + dy, pos[1] + dx) for dy, dx in DIRECTIONS)
                    if 0 <= r < self.size[0]
                    and 0 <= c < self.size[1])

    @staticmethod
    def parse(data: Iterable[str]) -> Cave:
        return Cave(([int(char) for char in line] for line in data))


#


def binary_insertion(val: Any, items: List[Any]) -> None:
    left = 0
    right = len(items)
    while left < right:
        m = int((left + right) / 2)
        if items[m] > val:
            right = m
        elif items[m] < val:
            left = m + 1
        else:
            items.insert(m, val)
            return
    items.insert(left, val)


def get_goal_distance(cave: Cave, pos: Tuple[int, int]) -> int:
    return sum(cave.size[i] - pos[i] for i in range(2))


def get_path(cave: Cave) -> List[Tuple[int, int]]:
    back_mapping: Dict[Tuple[int, int], Tuple[int, Optional[Tuple[int, int]]]] = {(0, 0): (0, None)}
    # Not going to bother implementing this as a true heap
    heap: List[Tuple[int, Tuple[int, int]]] = [(get_goal_distance(cave, (0, 0)), (0, 0))]
    visited: Set[Tuple[int, int]] = set()
    goal = tuple(x - 1 for x in cave.size)

    while len(heap) > 0:
        value, pos = heap.pop(0)
        if pos in visited:
            continue

        visited.add(pos)
        if pos == goal:
            break

        path_cost, back = back_mapping[pos]

        for adj, adj_cost in cave.get_adjacent_positions(pos):

            # Check if the path leading up to the current position and then to this adjacent one is shorter
            # than the adjacent position's previous best known route
            if adj in back_mapping:
                adj_back_g, adj_back = back_mapping[adj]
                if adj_back_g > path_cost + adj_cost:
                    back_mapping[adj] = (path_cost + adj_cost, pos)
            else:
                back_mapping[adj] = (path_cost + adj_cost, pos)

            if adj not in visited:
                binary_insertion((back_mapping[adj][0] + get_goal_distance(cave, adj), adj), heap)

    if goal not in back_mapping:
        raise Exception("PATH NOT FOUND.")

    path = []
    pos = goal
    while (0, 0) not in path:
        path.append(pos)
        path_cost, pos = back_mapping[pos]

    return list(reversed(path))
