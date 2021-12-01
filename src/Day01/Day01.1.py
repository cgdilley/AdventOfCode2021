from Utility import IntegerInputLoader

increases = 0
window = []

with IntegerInputLoader(day=1) as reader:
    for depth in reader:
        if len(window) < 3:
            window.append(depth)
            continue

        previous = sum(window)
        window.pop(0)
        window.append(depth)
        if sum(window) > previous:
            increases += 1

print(increases)
