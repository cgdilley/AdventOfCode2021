from __future__ import annotations

from typing import List, Set, Dict, Tuple, Optional, Union, Iterable, Iterator, Callable, Hashable
from abc import ABC, abstractmethod
from enum import Enum

from Utility import Coord, group_by


class Square:
    class Type(Enum):
        WALL = 0
        HALL = 1
        ENTRANCE = 2
        ROOM = 3

    def __init__(self, t: Square.Type, pos: Coord):
        self.pos = pos
        self.type = t

    def __str__(self) -> str:
        return "." if self.is_passable() else "#"

    def __repr__(self) -> str:
        return str(self)

    def is_passable(self) -> bool:
        return self.type != Square.Type.WALL


class Amphipod(Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"

    def __lt__(self, other) -> bool:
        return self.name < other.name

    def movement_cost(self, distance: int) -> int:
        if self == Amphipod.AMBER:
            return distance
        if self == Amphipod.BRONZE:
            return distance * 10
        if self == Amphipod.COPPER:
            return distance * 100
        if self == Amphipod.DESERT:
            return distance * 1000
        raise Exception("Unknown flavor")


class Path(Iterable[Coord]):

    def __init__(self, *steps: Coord):
        self.steps = list(steps)

    def __iter__(self) -> Iterator[Coord]:
        return iter(self.steps)

    def __len__(self) -> int:
        return len(self.steps) - 1

    def __getitem__(self, index: Union[int, slice]) -> Union[Coord, List[Coord]]:
        return self.steps[index]

    @property
    def start(self) -> Coord:
        return self.steps[0]

    @property
    def end(self) -> Coord:
        return self.steps[-1]

    def move(self) -> Move:
        return Move(self[0], self[-1])

    @classmethod
    def wrapper(cls, func: Callable[[..., ...], Iterable[Tuple[int, int]]]) -> Callable[[..., ...], Path]:
        def _wrapped(*args, **kwargs) -> Path:
            return Path(*(Coord(t) for t in func(*args, **kwargs)))

        return _wrapped


#


class Board:

    def __init__(self, *squares: Square):
        self.map: Dict[Coord, Square] = {s.pos: s for s in squares}
        self.amphipods: Dict[Coord, Amphipod] = dict()
        self.size = (max(p.r for p in self.map.keys()) + 1,
                     max(p.c for p in self.map.keys()) + 1)

        rooms: Dict[int, List[Square]] = group_by((s for s in squares if s.type == Square.Type.ROOM),
                                                  lambda s: s.pos.c)
        flavors = list(Amphipod)
        self.goals: Dict[Amphipod, Set[Coord]] = {
            flavors[i]: {s.pos for s in squares}
            for i, (col, squares) in enumerate(rooms.items())
        }
        self._path_cache: Dict[Tuple[Coord, Coord], Path] = dict()
        self._moves = {
            s1.pos: [
                Move(s1.pos, s2.pos)
                for s2 in squares if s2.is_passable() and s2.pos != s1.pos
            ]
            for s1 in squares if s1.is_passable()
        }

    def add_amphipods(self, *pairings: Tuple[Coord, Amphipod]):
        for c, a in pairings:
            self.add_amphipod(c, a)
        return self

    def add_amphipod(self, pos: Coord, amphipod: Amphipod) -> Board:
        self.amphipods[pos] = amphipod
        return self

    def is_home(self, pos: Coord, amphipod: Amphipod) -> bool:
        return pos in self.goals[amphipod]

    def snapshot(self) -> BoardSnapshot:
        return BoardSnapshot.snapshot(self)

    def get_path(self, from_pos: Coord, to_pos: Coord) -> Path:
        signature = (from_pos, to_pos)
        try:
            return self._path_cache[signature]
        except KeyError:
            path = self._generate_path(from_pos, to_pos)
            self._path_cache[signature] = path
            return path

    @Path.wrapper
    def _generate_path(self, from_pos: Coord, to_pos: Coord) -> Path:
        if from_pos not in self.map or to_pos not in self.map:
            raise Exception("Invalid path")
        lat_dir = 1 if to_pos.c > from_pos.c else -1
        if from_pos.r > 1 and to_pos.r > 1:
            if from_pos.c != to_pos.c:
                for r in range(from_pos.r, 1, -1):
                    yield r, from_pos.c
                for c in range(from_pos.c, to_pos.c, lat_dir):
                    yield 1, c
                for r in range(1, to_pos.r + 1):
                    yield r, to_pos.c
            else:
                vert_dir = 1 if to_pos.r > from_pos.r else -1
                for r in range(from_pos.r, to_pos.r + vert_dir, vert_dir):
                    yield r, from_pos.c
        elif from_pos.r > to_pos.r:
            for r in range(from_pos.r, to_pos.r, -1):
                yield r, from_pos.c
            for c in range(from_pos.c, to_pos.c + lat_dir, lat_dir):
                yield to_pos.r, c
        else:
            for c in range(from_pos.c, to_pos.c, lat_dir):
                yield from_pos.r, c
            for r in range(from_pos.r, to_pos.r + 1):
                yield r, to_pos.c

    def is_valid_path(self, path: Path) -> bool:
        return all(rule.is_valid(self, path) for rule in RULES)

    def get_unchecked_options(self) -> Iterable[Move]:
        for a_pos in self.amphipods.keys():
            yield from self._moves[a_pos]
        # for s in self._passable:
        #     for a_pos in self.amphipods.keys():
        #         if s.pos != a_pos:
        #             yield Move(a_pos, s.pos)

    def get_valid_options(self) -> Iterable[Path]:
        for m in self.get_unchecked_options():
            path = self.get_path(m.from_, m.to_)
            if self.is_valid_path(path):
                yield path

    def move(self, m: Move):
        # if m.from_ not in self.amphipods:
        #     raise Exception("Invalid move")
        a = self.amphipods[m.from_]
        del self.amphipods[m.from_]
        self.amphipods[m.to_] = a

    def render(self):
        height, width = self.size
        for row in range(height):
            line = ""
            for col in range(width):
                coord = Coord.of(row, col)
                if coord in self.amphipods:
                    line += self.amphipods[coord].value
                elif coord in self.map:
                    if self.map[coord].is_passable():
                        line += "."
                    else:
                        line += "#"
                else:
                    line += " "
            print(line)
        print()

    @classmethod
    def parse(cls, data: List[str]) -> Board:
        squares: List[Square] = []
        amphipods: List[Tuple[Amphipod, Coord]] = []
        for row, line in enumerate(data):
            for col, char in enumerate(line):
                if char == "#":
                    squares.append(Square(Square.Type.WALL, Coord.of(row, col)))
                elif char in ("A", "B", "C", "D"):
                    squares.append(Square(Square.Type.ROOM, Coord.of(row, col)))
                    amphipods.append((Amphipod(char), Coord.of(row, col)))
                elif char == ".":
                    if data[row + 1][col] in ("A", "B", "C", "D"):
                        squares.append(Square(Square.Type.ENTRANCE, Coord.of(row, col)))
                    else:
                        squares.append(Square(Square.Type.HALL, Coord.of(row, col)))
        b = Board(*squares)
        for a, pos in amphipods:
            b.add_amphipod(pos, a)
        return b

    def load_snapshot(self, snapshot: BoardSnapshot):
        self.amphipods.clear()
        self.add_amphipods(*((p, Amphipod(f))
                             for f, p in snapshot.state))

    @staticmethod
    def from_snapshot(snapshot: BoardSnapshot) -> Board:
        return Board(*snapshot.map.values()) \
            .add_amphipods(*((p, Amphipod(f))
                             for f, p in snapshot.state))


class BoardSnapshot(Hashable):

    def __init__(self, board: Board,
                 state: Tuple[Tuple[Amphipod, Coord], ...]):
        self.map = board.map
        self.state = state

    def __hash__(self) -> int:
        return hash(self.state)

    def __eq__(self, other) -> bool:
        return isinstance(other, BoardSnapshot) and other.state == self.state

    def __lt__(self, other) -> bool:
        return isinstance(other, BoardSnapshot) and self.state < other.state

    def __str__(self) -> str:
        return str(self.state)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def snapshot(board: Board) -> BoardSnapshot:
        return BoardSnapshot(board, tuple(sorted((a, c) for c, a in board.amphipods.items())))


class Move(Hashable):

    def __init__(self, from_pos: Coord, to_pos: Coord):
        self.from_ = from_pos
        self.to_ = to_pos

    def __hash__(self) -> int:
        return hash((self.from_, self.to_))

    def __eq__(self, other) -> bool:
        return isinstance(other, Move) and other.from_ == self.from_ and other.to_ == self.to_

    def __str__(self) -> str:
        return f"{self.from_} -> {self.to_}"

    def __repr__(self) -> str:
        return str(self)


class PathRule(ABC):

    @abstractmethod
    def is_valid(self, board: Board, path: Path) -> bool: ...


class ExistsRule(PathRule):

    def is_valid(self, board: Board, path: Path) -> bool:
        return all(pos in board.map for pos in path)


class EntranceStopRule(PathRule):

    def is_valid(self, board: Board, path: Path) -> bool:
        return board.map[path.end].type != Square.Type.ENTRANCE


class ClearPathRule(PathRule):

    def is_valid(self, board: Board, path: Path) -> bool:
        return all(pos not in board.amphipods
                   for pos in path[1:])


class ValidRoomRule(PathRule):

    _CACHE: Dict[Tuple[Amphipod, Move], bool] = dict()

    def is_valid(self, board: Board, path: Path) -> bool:
        a = board.amphipods[path.start]
        signature = (a, path.move())

        try:
            return self._CACHE[signature]
        except KeyError:

            try:
                first_non_room = [board.map[pos].type == Square.Type.ROOM
                                  for pos in path].index(False)
                result = all(board.is_home(pos, a)
                             for pos in path[first_non_room:]
                             if board.map[pos].type == Square.Type.ROOM)
            except ValueError:
                result = True

            self._CACHE[signature] = result
            return result


class HallwayRule(PathRule):

    def is_valid(self, board: Board, path: Path) -> bool:
        return not (board.map[path.start].type == board.map[path.end].type == Square.Type.HALL)

# class AtHomeRule(PathRule):
#
#     @classmethod
#     def is_valid(cls, board: Board, path: Path) -> bool:
#         return not (path.start in board.amphipods[path.start].destination and
#                     path[0].c == 3)


RULES = [
    EntranceStopRule(),
    ClearPathRule(),
    ValidRoomRule(),
    HallwayRule()
]
