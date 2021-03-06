from __future__ import annotations

from Utility.MovementCommand import MovementCommand

from typing import Iterable, Iterator, TextIO, Optional, Generic, TypeVar
import os

T = TypeVar('T')


class InputLoader(Iterator[T], Generic[T]):

    def __init__(self, day: int, sample: bool = False, alternate_source: str = None):
        self.day = day
        self.sample = sample
        self.alternate_source = alternate_source
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
        suffix = '' if not self.sample else '-sample'
        if self.alternate_source is not None:
            suffix += f"({self.alternate_source})"
        return os.path.join(directory, f"[day{str(self.day).rjust(2, '0')}]input{suffix}.txt")

    def is_open(self) -> bool:
        return self._file is not None

    def process_line(self, line: str) -> T:
        return line.strip("\n")

    def skip_line(self) -> None:
        _ = next(self)


class IntegerInputLoader(InputLoader[int]):

    def process_line(self, line: str) -> int:
        return int(super().process_line(line))


class MovementCommandInputLoader(InputLoader[MovementCommand]):

    def process_line(self, line: str) -> MovementCommand:
        return MovementCommand.parse(super().process_line(line))


class BytesInputLoader(InputLoader[bin]):

    def open(self):
        if self.is_open():
            return
        self._file = open(self.get_filename(), "rb")

    def __next__(self) -> bin:
        self.open()
        b = self._file.read(1)
        if b == b"":
            raise StopIteration
        return b
