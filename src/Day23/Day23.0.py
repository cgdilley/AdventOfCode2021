from Utility import InputLoader
from Utility.Helpers import binary_insertion
from Utility.Coord import Coord

from Day23.Day23Shared import Board, Square, Amphipod, BoardSnapshot, Move
from typing import Set, Tuple, List, Iterable, Optional, Dict
from abc import ABC, abstractmethod


def main():
    with InputLoader(day=23, sample=False) as reader:
        lines = list(reader)

    board = Board.parse(lines)
    # board.render()

    snap = board.snapshot()

    visited: Set[BoardSnapshot] = set()
    stack = SortedStackManager()
    stack.push(snap, 0)
    # stack: List[Tuple[int, BoardSnapshot]] = [(0, snap)]
    back_map: Dict[BoardSnapshot, Optional[Tuple[int, BoardSnapshot]]] = {snap: (0, None)}

    while len(stack) > 0:
        snap = stack.pop()
        if snap in visited:
            continue
        visited.add(snap)
        b = Board.from_snapshot(snap)
        travelled, back_snap = back_map[snap] if snap in back_map else (0, None)

        if all(a.is_home() for a in b.amphipods.values()):
            route = [snap]
            while True:
                dist, s = back_map[route[-1]]
                if s is None:
                    break
                route.append(s)
            for bs in reversed(route):
                Board.from_snapshot(bs).render()
            print(f"TRAVELLED = {travelled}")
            break
        options = list(b.get_valid_options())
        for path in options:
            cost = b.amphipods[path[0]].movement_cost(len(path)-1)
            b.move(path.move())
            new_snap = b.snapshot()
            goal_distance = distance_from_goal(b)
            b.move(Move(path[-1], path[0]))
            # Board.from_snapshot(new_snap).render()
            if new_snap not in back_map or back_map[new_snap][0] > travelled + cost:
                back_map[new_snap] = (travelled + cost, snap)
            stack.push(new_snap, travelled + cost + goal_distance)


def distance_from_goal(b: Board) -> int:
    total = 0
    # return 0
    for a in b.amphipods.values():
        if a.is_home():
            continue
        dist = len(b.get_path(a.pos, min(p for p in a.destination)))
        # dist = min(a.pos.distance(p) for p in a.destination)
        total += a.movement_cost(dist)
    return total


class StackManager(ABC):

    def __init__(self):
        self.stack: List[Tuple[int, BoardSnapshot]] = []

    def __len__(self) -> int:
        return len(self.stack)

    @abstractmethod
    def push(self, snap: BoardSnapshot, value: int): ...

    @abstractmethod
    def pop(self) -> BoardSnapshot: ...

    def pop_at(self, index: int) -> BoardSnapshot:
        _, snap = self.stack.pop(index)
        return snap


class SortedStackManager(StackManager):

    def push(self, snap: BoardSnapshot, value: int):
        binary_insertion((value, snap), self.stack)

    def pop(self) -> BoardSnapshot:
        return self.pop_at(0)


class UnsortedStackManager(StackManager):

    def push(self, snap: BoardSnapshot, value: int):
        self.stack.append((value, snap))

    def pop(self) -> BoardSnapshot:
        min_val = None
        min_index = 0
        for i, (val, snap) in enumerate(self.stack):
            if min_val is None or val < min_val:
                min_val = val
                min_index = i
        return self.pop_at(min_index)


#


#


if __name__ == '__main__':
    main()
