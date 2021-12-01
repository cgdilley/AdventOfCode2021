from Utility import IntegerInputLoader

from typing import Optional

previous: Optional[int] = None
increases = 0

with IntegerInputLoader(day=1) as reader:
    for depth in reader:
        if previous is not None and depth > previous:
            increases += 1
        previous = depth

print(increases)
