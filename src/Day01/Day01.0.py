from Utility import IntegerInputLoader

from typing import Optional

previous: Optional[int] = None
increases = 0

for depth in IntegerInputLoader(day=1):
    if previous is not None and depth > previous:
        increases += 1
    previous = depth

print(increases)
