from __future__ import annotations

from typing import List, Tuple, Iterable, Iterator, Dict, Set, Optional


class Image:

    def __init__(self, pixels: List[List[bool]], infinite_state: bool):
        self.pixels = pixels
        self.infinite_state = infinite_state

    @property
    def size(self) -> Tuple[int, int]:
        return len(self.pixels), len(self.pixels[0]) if len(self.pixels) > 0 else 0

    def enhance(self, algorithm: List[bool]) -> Image:
        new_pixels: List[List[bool]] = []
        height, width = self.size
        for r in range(-1, height+2):
            new_pixels.append([self.enhance_pixel(r, c, algorithm)
                               for c in range(-1, width+2)])
        return Image(new_pixels, algorithm[-1] if self.infinite_state else algorithm[0])

    def enhance_pixel(self, row: int, col: int, algorithm: List[bool]) -> bool:
        region = "".join("1" if x else "0" for x in self.read_region(row, col))
        index = int(region, 2)
        return algorithm[index]

    def read_region(self, row: int, col: int) -> Iterable[bool]:
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                yield self.get_pixel_at(r, c)

    def get_pixel_at(self, row: int, col: int) -> bool:
        if 0 <= row < len(self.pixels) and 0 <= col < len(self.pixels[row]):
            return self.pixels[row][col]
        return self.infinite_state

    def pixel_columns(self) -> List[List[bool]]:
        height, width = self.size
        columns: List[List[bool]] = []
        for c in range(0, width):
            columns.append([self.pixels[r][c] for r in range(height)])
        return columns

    def trim(self):
        while all(x == self.infinite_state for x in self.pixels[0]):
            self.pixels.pop(0)
        while all(x == self.infinite_state for x in self.pixels[-1]):
            self.pixels.pop(-1)
        while all(x[0] == self.infinite_state for x in self.pixels):
            self.pixels = [r[1:] for r in self.pixels]
        while all(x[-1] == self.infinite_state for x in self.pixels):
            self.pixels = [r[:-1] for r in self.pixels]
        # left = min(r.index(not self.infinite_state) for r in self.pixels)
        # right = min(r[::-1].index(not self.infinite_state) for r in self.pixels)
        # columns = self.pixel_columns()
        # top = min(c.index(not self.infinite_state) for c in columns)
        # bottom = min(c[::-1].index(not self.infinite_state) for c in columns)
        # self.pixels = [r[left:-right] for r in self.pixels[top:-bottom]]

    def count_lit(self) -> int:
        return sum(1 if c else 0 for r in self.pixels for c in r)

    def render(self) -> None:
        height, width = self.size
        print("." * (width + 2))
        for r in self.pixels:
            print("." + "".join("#" if c else '.' for c in r) + ".")
        print("." * (width + 2))

    @classmethod
    def parse(cls, data: Iterable[str]) -> Image:
        return Image([cls.line_to_binary_list(line) for line in data], False)

    @staticmethod
    def line_to_binary_list(line: str) -> List[bool]:
        return [True if c == "#" else False for c in line]
