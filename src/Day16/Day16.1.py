
from Utility import BytesInputLoader


from Day16.Day16Shared import Packet, Literal, Operator


def main():
    with BytesInputLoader(day=16) as reader:
        packet = Packet.parse_from_bytes(reader)

    print(f"VALUE = {packet.get_value()}")


#


#


#


if __name__ == '__main__':
    main()
