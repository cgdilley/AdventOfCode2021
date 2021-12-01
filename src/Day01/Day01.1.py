from Utility import IntegerInputLoader

increases = 0
window = []

for depth in IntegerInputLoader(day=1):
    if len(window) < 3:
        window.append(depth)
        continue

    previous = sum(window)
    window.pop(0)
    window.append(depth)
    if sum(window) > previous:
        increases += 1

print(increases)
