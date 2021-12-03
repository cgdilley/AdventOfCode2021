
from Utility import InputLoader

count = []

with InputLoader(day=3) as reader:
    for line in reader:
        for i, char in enumerate(line):
            if len(count) <= i:
                count.append({"0": 0, "1": 0})
            count[i][char] += 1

gamma_str = "".join("1" if x["1"] >= x["0"] else "0" for x in count)
epsilon_str = "".join("1" if x["1"] < x["0"] else "0" for x in count)

gamma = int(gamma_str, 2)
epsilon = int(epsilon_str, 2)

print(f"GAMMA = {gamma}, EPSILON = {epsilon}")
print(f"MULTIPLIED = {gamma * epsilon}")
