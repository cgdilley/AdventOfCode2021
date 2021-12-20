
from Utility import InputLoader

from Day19.Day19Shared import BeaconCoord, Scanner


def main():
    with InputLoader(day=19) as reader:
        scanners = []
        while reader.is_open():
            scanners.append(Scanner.parse(reader))

    for s1 in scanners:
        for s2 in scanners:
            # if s1 == s2:
            #     continue
            overlap = s1.overlap(s2)
            if overlap >= 12:
                print("WOAH OVERLAP")

    print(scanners)


#


#


if __name__ == '__main__':
    main()
