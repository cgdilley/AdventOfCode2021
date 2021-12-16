from __future__ import annotations

import getpass
from typing import Iterable, List, Set, Dict, Tuple, Optional, Iterator, Generic, TypeVar
from abc import ABC, abstractmethod
import functools


class Packet(ABC):

    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id

    @staticmethod
    def read(data: Iterator[str], amount: int) -> str:
        return "".join(next(data) for _ in range(amount))

    @classmethod
    def parse_from_bytes(cls, bin_data: Iterable[bin]) -> Packet:
        return cls.parse_from_hex((b.decode() for b in bin_data))

    @classmethod
    def parse_from_hex(cls, hex_str: Iterable[str]) -> Packet:
        return cls.parse(iter(hex_to_bin(hex_str)))

    @classmethod
    def parse(cls, data: Iterator[str]) -> Packet:
        version = int(cls.read(data, 3), 2)
        type_id = int(cls.read(data, 3), 2)
        if type_id == Literal.TYPE_ID:
            return Literal.parse_literal(data, version)
        else:
            return Operator.parse_operator(data, version, type_id)

    @abstractmethod
    def get_version_sum(self) -> int: ...

    @abstractmethod
    def get_value(self) -> int: ...


class Literal(Packet):

    TYPE_ID = 4

    def __init__(self, version: int, value: int):
        super(Literal, self).__init__(version, self.TYPE_ID)
        self.value = value

    @classmethod
    def parse_literal(cls, data: Iterator[str], version: int) -> Literal:
        value = ""
        while True:
            chunk = cls.read(data, 5)
            value += chunk[1:]
            if chunk.startswith("0"):
                break
        return Literal(version, int(value, 2))

    def get_version_sum(self) -> int:
        return self.version

    def get_value(self) -> int:
        return self.value


class Operator(Packet, ABC):

    def __init__(self, version: int, type_id: int, sub_packets: List[Packet]):
        super(Operator, self).__init__(version, type_id)
        self.sub_packets = sub_packets

    @classmethod
    def parse_operator(cls, data: Iterator[str], version: int, type_id: int) -> Operator:
        packets = []
        length_type_id = next(data)
        if length_type_id == "0":
            length = int(cls.read(data, 15), 2)
            chunk = SubIterator(data, length)
            while True:
                try:
                    sub_packet = Packet.parse(chunk)
                    packets.append(sub_packet)
                except RuntimeError as e:
                    if hasattr(e, "args") and len(e.args) > 0 and e.args[0].endswith("StopIteration"):
                        break
                    raise
        else:
            count = int(cls.read(data, 11), 2)
            for i in range(count):
                sub_packet = Packet.parse(data)
                packets.append(sub_packet)

        return OPERATOR_TYPE_MAPPING[type_id](version, type_id, packets)

    def get_version_sum(self) -> int:
        return self.version + sum(p.get_version_sum() for p in self.sub_packets)

    def _values(self) -> Iterable[int]:
        return (p.get_value() for p in self.sub_packets)


class SumOperator(Operator):

    def get_value(self) -> int:
        return sum(self._values())


class ProductOperator(Operator):

    def get_value(self) -> int:
        return functools.reduce(lambda a, b: a * b, self._values(), 1)


class MinimumOperator(Operator):

    def get_value(self) -> int:
        return min(self._values())


class MaximumOperator(Operator):

    def get_value(self) -> int:
        return max(self._values())


class GreaterThanOperator(Operator):

    def get_value(self) -> int:
        return 1 if self.sub_packets[0].get_value() > self.sub_packets[1].get_value() else 0


class LessThanOperator(Operator):

    def get_value(self) -> int:
        return 1 if self.sub_packets[0].get_value() < self.sub_packets[1].get_value() else 0


class EqualsOperator(Operator):

    def get_value(self) -> int:
        return 1 if self.sub_packets[0].get_value() == self.sub_packets[1].get_value() else 0


OPERATOR_TYPE_MAPPING = {
    0: SumOperator,
    1: ProductOperator,
    2: MinimumOperator,
    3: MaximumOperator,
    5: GreaterThanOperator,
    6: LessThanOperator,
    7: EqualsOperator
}


def hex_to_bin(hex_str: Iterable[str]) -> Iterable[str]:
    for char in hex_str:
        raw_int = int(char, 16)
        binary = format(raw_int, "0>4b")
        yield from binary


T = TypeVar('T')


class SubIterator(Iterator[T], Generic[T]):

    def __init__(self, parent: Iterator[T], length: int):
        self.parent = parent
        self.length = length
        self.pos = 0

    def __next__(self) -> T:
        if self.pos >= self.length:
            raise StopIteration
        self.pos += 1
        return next(self.parent)
