
from Utility import MovementCommand, MovementCommandInputLoader

position = (0, 0)

with MovementCommandInputLoader(day=2) as reader:
    for command in reader:
        position = command.adjust_direct(position)

print("POSITION = %dh, %dd" % position)

print(f"MULTIPLIED = {position[0] * position[1]}")
