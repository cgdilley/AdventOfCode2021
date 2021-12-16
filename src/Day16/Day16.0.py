
from Utility import InputLoader


from Day16.Day16Shared import Packet, Literal, Operator


def main():
    with InputLoader(day=16) as reader:
        data = next(reader).strip()

    packet = Packet.parse_from_hex(data)

    print(f"VERSION SUM = {packet.get_version_sum()}")


#


#


#


if __name__ == '__main__':
    main()
