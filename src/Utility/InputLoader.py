from __future__ import annotations

from typing import Iterable, Iterator, TextIO, Optional, Generic, TypeVar
import os
from abc import ABC, abstractmethod

T = TypeVar('T')


class InputLoader(Iterator[T], Generic[T], ABC):

    def __init__(self, day: int):
        self.day = day
        self._file: Optional[TextIO] = None

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        self.open()
        try:
            return self.process_line(next(self._file))
        except StopIteration:
            self.close()
            raise

    def __enter__(self) -> InputLoader[T]:
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def open(self):
        if self.is_open():
            return
        self._file = open(self.get_filename(), "r", encoding="utf-8")

    def close(self):
        if not self.is_open():
            return
        self._file.close()
        self._file = None

    def get_filename(self, directory: str = "../../input") -> str:
        return os.path.join(directory, f"[day{str(self.day).rjust(2, '0')}]input.txt")

    def is_open(self) -> bool:
        return self._file is not None

    def process_line(self, line: str) -> T:
        return line.strip()


class IntegerInputLoader(InputLoader[int]):

    def __iter__(self) -> Iterable[int]:
        return self

    def __next__(self) -> int:
        return super().__next__()

    def process_line(self, line: str) -> int:
        return int(super().process_line(line))
