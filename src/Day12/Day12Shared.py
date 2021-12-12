from __future__ import annotations

from typing import List, Iterable, Set, Tuple, Dict, Optional
from enum import Enum


class Cave:

    class CaveType(Enum):
        START = 0
        END = 1
        BIG = 2
        SMALL = 3

    def __init__(self, title: str):
        self.title = title
        self._paths: Dict[str, Cave] = dict()

    def __contains__(self, name: str) -> bool:
        return name in self._paths

    def __getitem__(self, name: str) -> Optional[Cave]:
        return self._paths[name] if name in self._paths else None

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other) -> bool:
        return isinstance(other, Cave) and other.title == self.title

    def __lt__(self, other) -> bool:
        return isinstance(other, Cave) and self.title < other.title

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return str(self)

    @property
    def type(self) -> CaveType:
        if self.title == "start":
            return Cave.CaveType.START
        elif self.title == "end":
            return Cave.CaveType.END
        elif self.title.isupper():
            return Cave.CaveType.BIG
        else:
            return Cave.CaveType.SMALL

    def add_path(self, cave: Cave):
        self._paths[cave.title] = cave

    def all_paths(self) -> Iterable[Cave]:
        yield from self._paths.values()

    def is_big(self) -> bool:
        return self.type == Cave.CaveType.BIG

    def is_small(self) -> bool:
        return self.type == Cave.CaveType.SMALL

    def is_start(self) -> bool:
        return self.type == Cave.CaveType.START

    def is_end(self) -> bool:
        return self.type == Cave.CaveType.END


#


class CaveSystem:

    def __init__(self):
        self._caves: Dict[str, Cave] = dict()

    def __getitem__(self, name: str) -> Cave:
        if name not in self._caves:
            self._caves[name] = Cave(name)
        return self._caves[name]

    @staticmethod
    def parse(data: Iterable[str]) -> CaveSystem:
        cs = CaveSystem()
        for line in data:
            _from, _to = line.split("-")
            cs[_from].add_path(cs[_to])
            cs[_to].add_path(cs[_from])
        return cs
