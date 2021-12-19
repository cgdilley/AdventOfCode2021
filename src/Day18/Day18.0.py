
from Utility import InputLoader

from Day18.Day18Shared import SnailPair


def main():
    with InputLoader(day=18, sample=True) as reader:
        pairs = [SnailPair.parse(line) for line in reader]

    result = pairs[0]
    for i in range(len(pairs)-1):
        result += pairs[i+1]
    print(str(result))

    print(f"MAGNITUDE = {result.magnitude()}")

#


#


if __name__ == '__main__':
    main()
