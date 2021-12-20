
from Utility import InputLoader

from Day20.Day20Shared import Image


def main():
    with InputLoader(day=20, sample=False) as reader:
        algorithm = Image.line_to_binary_list(next(reader))
        reader.skip_line()
        image = Image.parse(reader)

    image.trim()
    for _ in range(50):
        image = image.enhance(algorithm)
        image.trim()

    image.render()
    print(f"NUMBER OF LIT PIXELS IN OUTPUT: {image.count_lit()}")


#


#


if __name__ == '__main__':
    main()
