from __future__ import annotations

from Utility import InputLoader
from Utility.Helpers import binary_insertion
from Utility.Coord import Coord

from Day23.Day23Shared import Board, Square, Amphipod, BoardSnapshot, Move
from typing import Set, Tuple, List, Iterable, Optional, Dict
from abc import ABC, abstractmethod
from pyinstrument import Profiler


def main():
    with InputLoader(day=23, sample=True) as reader:
        lines = list(reader)

    # profiler = Profiler()
    # profiler.start()

    board = Board.parse(lines)
    board.render()

    snap = board.snapshot()

    visited: Set[BoardSnapshot] = set()
    stack = SortedStackManager()
    stack.push(snap, (0, 0))
    # stack: List[Tuple[int, BoardSnapshot]] = [(0, snap)]
    # back_map: Dict[BoardSnapshot, Optional[Tuple[int, BoardSnapshot]]] = {snap: (0, None)}
    back_stack = BackStack()
    back_stack.set_root(snap)

    while len(stack) > 0:
        snap = stack.pop()
        if snap in visited:
            continue
        visited.add(snap)

        print(f"VISITED = {len(visited)}, IN STACK = {len(stack)}")

        board.load_snapshot(snap)
        back_pointer = back_stack[snap]

        if all(board.is_home(c, a) for c, a in board.amphipods.items()):
            for bs in back_stack.route(snap):
                Board.from_snapshot(bs).render()
            print(f"TRAVELLED = {back_pointer.cost}")
            break

        for path in board.get_valid_options():
            cost = board.amphipods[path.start].movement_cost(len(path))
            board.move(path.move())
            new_snap = board.snapshot()
            goal_distance = distance_from_goal(board)
            # board.render()
            board.move(Move(path.end, path.start))

            back_stack.insert(new_snap, snap, back_pointer.cost + cost)
            if new_snap not in visited:
                stack.push(new_snap, (back_pointer.cost + cost + goal_distance,))

    # profiler.stop()

    # print(profiler.output_text(unicode=True, color=True))


def distance_from_goal(b: Board) -> int:
    total = 0
    # return 0
    for c, a in b.amphipods.items():
        if b.is_home(c, a):
            continue
        path = b.get_path(c, min(p for p in b.goals[a]))
        dist = len(path)
        # dist = min(a.pos.distance(p) for p in a.destination)
        total += a.movement_cost(dist)

        # overlaps = sum(1 for pos in path[1:] if pos.r > 1 and pos in b.amphipods)
        # total += a.movement_cost(overlaps)
    return total


class StackManager(ABC):

    def __init__(self):
        self.stack: List[Tuple[Tuple[int, ...], BoardSnapshot]] = []

    def __len__(self) -> int:
        return len(self.stack)

    @abstractmethod
    def push(self, snap: BoardSnapshot, value: Tuple[int, ...]): ...

    @abstractmethod
    def pop(self) -> BoardSnapshot: ...

    def pop_at(self, index: int) -> BoardSnapshot:
        _, snap = self.stack.pop(index)
        return snap


class SortedStackManager(StackManager):

    def push(self, snap: BoardSnapshot, value: Tuple[int, ...]):
        binary_insertion((value, snap), self.stack)

    def pop(self) -> BoardSnapshot:
        return self.pop_at(0)


class UnsortedStackManager(StackManager):

    def push(self, snap: BoardSnapshot, value: Tuple[int, ...]):
        self.stack.append((value, snap))

    def pop(self) -> BoardSnapshot:
        min_val = None
        min_index = 0
        for i, (val, snap) in enumerate(self.stack):
            if min_val is None or val < min_val:
                min_val = val
                min_index = i
        return self.pop_at(min_index)


class BackStackElement:

    def __init__(self, pointer: Optional[BoardSnapshot], cost: int):
        self.pointer = pointer
        self.cost = cost

    @staticmethod
    def null() -> BackStackElement:
        return BackStackElement(None, 0)


class BackStack:

    def __init__(self):
        self.stack: Dict[BoardSnapshot, Optional[BackStackElement]] = dict()

    def __contains__(self, item: BoardSnapshot) -> bool:
        return item in self.stack

    def __getitem__(self, item: BoardSnapshot) -> BackStackElement:
        return self.get(item)

    def set_root(self, snap: BoardSnapshot):
        self.stack[snap] = BackStackElement.null()

    def insert(self, from_snap: BoardSnapshot, to_snap: BoardSnapshot, cost: int):
        try:
            if self[from_snap].cost > cost:
                self.stack[from_snap] = BackStackElement(to_snap, cost)
        except KeyError:
            self.stack[from_snap] = BackStackElement(to_snap, cost)

    def get(self, from_snap: BoardSnapshot) -> BackStackElement:
        return self.stack[from_snap]

    def route(self, to_snap: BoardSnapshot) -> List[BoardSnapshot]:
        route = [to_snap]
        while True:
            pointer = self.get(route[0])
            if pointer.pointer is None:
                break
            route.insert(0, pointer.pointer)
        return route


#


#


if __name__ == '__main__':
    main()
