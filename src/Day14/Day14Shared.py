from __future__ import annotations


class Instruction:

    def __init__(self, pair: str, addition: str):
        self.pair = pair
        self.addition = addition

    def __str__(self) -> str:
        return f"{self.pair} -> {self.addition}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def result(self) -> str:
        return f"{self.pair[0]}{self.addition}{self.pair[1:]}"

    @staticmethod
    def parse(line: str):
        pair, result = line.split(" -> ")
        return Instruction(pair, result)
