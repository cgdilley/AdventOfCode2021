from Utility import InputLoader

import statistics
import math

with InputLoader(day=7) as reader:
    crabs = [int(x) for line in reader for x in line.split(",")]


def complicated_but_robust():
    """
    Makes a guess for the starting position, and starts looking around for the local minimum in terms of fuel consumed.
    Whatever position results in the minimum fuel consumption should be flanked by 2 positions that have
    greater or equal fuel consumption.

    Otherwise, follow the "slope" downwards towards this minimum.  This means that if for position X you have
    a fuel consumption greater than that for position X + 1, that means position X - 1 will be even greater and
    is not worth checking; instead look in the direction of position X + 2 until you find where it
    starts sloping back up again, and find that inflection point (which will be the minimum).

    Maybe could be made smarter by detecting the magnitude of the slope and adjusting the amount the "cursor" moves
    by, but doesn't appear to be necessary
    """

    center = statistics.mean(crabs)
    position = math.floor(center)
    direction = 1
    value_map = dict()

    while True:
        if position not in value_map:
            value_map[position] = sum(fuel_consumption(abs(c - position)) for c in crabs)

        if position - 1 in value_map and position + 1 in value_map:
            if value_map[position] < min(value_map[position - 1], value_map[position + 1]):
                break
            elif value_map[position] > value_map[position + 1]:
                position += 1
                direction = 1
            else:
                position -= 1
                direction = -1
        elif position - direction in value_map:
            if value_map[position] <= value_map[position - direction]:
                position += direction
            else:
                position -= direction
                direction *= -1
        elif position + direction in value_map:
            if value_map[position] <= value_map[position + direction]:
                position -= direction
                direction *= -1
            else:
                position += direction
        else:
            position += direction

    print(f"POSITION = {position}")
    fuel = sum(fuel_consumption(abs(c - position)) for c in crabs)
    print(f"FUEL CONSUMED = {fuel}")


#


def simple_but_unproven():
    """
    The mean of the values seems to end up being the center position.  However, I can't explain WHY that would be,
    so this solution might break under circumstances other than what I have available to me (because it works for
    those that I do).
    """
    center = statistics.mean(crabs)
    fuel = min(sum(fuel_consumption(abs(c - math.floor(center))) for c in crabs),
               sum(fuel_consumption(abs(c - math.ceil(center))) for c in crabs))
    print(f"CENTER = {center}")
    print(f"FUEL CONSUMED = {fuel}")


#


def fuel_consumption(dist: int) -> int:
    return int(((dist + 1) * dist) / 2)


def distance(fuel: int) -> int:
    return int(0.5 * ((((8 * fuel) + 1) ** 0.5) - 1))


#


if __name__ == '__main__':
    complicated_but_robust()
