
from Utility import InputLoader

import statistics
import math


with InputLoader(day=7) as reader:
    crabs = [int(x) for line in reader for x in line.split(",")]


median = statistics.median(crabs)

if len(crabs) % 2 == 0:
    fuel = sum(abs(x - median) for x in crabs)
else:
    fuel = min(sum(abs(x - math.floor(median)) for x in crabs),
               sum(abs(x - math.ceil(median)) for x in crabs))

print(f"FUEL CONSUMED: {fuel}")

