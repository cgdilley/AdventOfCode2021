from __future__ import annotations

from typing import Iterable, List, Tuple, Set, Optional, Dict, Iterator


class Scanner:

    def __init__(self, name: str, *beacons: BeaconCoord):
        self.name = name
        self.beacons = beacons
        self.distances = [[
            (abs(self.beacons[i].x - b.x),
             abs(self.beacons[i].y - b.y),
             abs(self.beacons[i].z - b.z))
            for i in range(len(self.beacons))]
            for b in self.beacons]

    def __eq__(self, other):
        return isinstance(other, Scanner) and self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def rotated(self, xr: int, yr: int, zr: int) -> Scanner:
        return Scanner(self.name, *(b.rotated(xr, yr, zr) for b in self.beacons))

    def overlap(self, other: Scanner) -> int:
        pass
        # return sum(1
        #            for i in range(len(self.beacons))
        #            if any(all(dist1[d] in dist2 for d in range(3))
        #                   for dist1 in self.distances[i]
        #                   for j in range(len(other.beacons))
        #                   for dist2 in other.distances[j]
        #                   if dist1 != (0, 0, 0)))

    @staticmethod
    def parse(data: Iterator[str]) -> Scanner:
        name = next(data)
        beacons = []
        for line in data:
            if not line:
                break
            beacons.append(BeaconCoord.parse(line))
        return Scanner(name, *beacons)


class BeaconCoord:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return isinstance(other, BeaconCoord) and self.x == other.x and self.y == other.y \
               and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self) -> str:
        return str(self)

    def rotated(self, xr: int, yr: int, zr: int) -> BeaconCoord:
        x = self.x
        y = self.y
        z = self.z
        if xr < 0:
            x = -self.x
            xr = ~xr
        if yr < 0:
            y = -self.y
            yr = ~yr
        if zr < 0:
            z = -self.z
            zr = ~zr

        def _rotate(amount: int, primary: int, secondary: int) -> Tuple[int, int]:
            amount = amount % 4
            if amount == 1:
                return -secondary, primary
            if amount == 2:
                return -primary, -secondary
            if amount == 3:
                return secondary, -primary

        y, z = _rotate(xr, y, z)
        z, x = _rotate(yr, z, x)
        x, y = _rotate(zr, x, y)

        return BeaconCoord(x, y, z)

    @staticmethod
    def parse(line: str) -> BeaconCoord:
        return BeaconCoord(*(int(x) for x in line.split(",")))
