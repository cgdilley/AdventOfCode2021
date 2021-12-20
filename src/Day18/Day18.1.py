
from Utility import InputLoader

from Day18.Day18Shared import SnailPair


def main():
    with InputLoader(day=18) as reader:
        pairs = [SnailPair.parse(line) for line in reader]

    biggest = max((x + y).magnitude()
                  for x in pairs for y in pairs if x != y)

    print(f"LARGEST MAGNITUDE = {biggest}")

#


#


if __name__ == '__main__':
    main()
