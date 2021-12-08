
from Utility import InputLoader
from Day08.Day08Shared import Reading, DIGIT_PATTERNS


with InputLoader(day=8) as reader:
    readings = [Reading.parse(line) for line in reader]


uniques = sum(sum(1 for o in r.output if len(o) in (2, 3, 4, 7)) for r in readings)
print("DIGITS WITH UNIQUE LENGTH: " + str(uniques))
