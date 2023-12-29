#!/usr/bin/env python3

from itertools import combinations

# Given numbers
numbers = [981, 894, 66, 35, 24, 15, 15, 6, 4, 4, 2, 1, 1]

# Target sum
target_sum = 1024

# Find combinations that sum up to the target
valid_combinations = []
for r in range(1, len(numbers) + 1):
    for combo in combinations(numbers, r):
        if sum(combo) == target_sum:
            remaining_numbers = [x for x in numbers]
            for i in combo:
                remaining_numbers.pop(remaining_numbers.index(i))
            if sum(remaining_numbers) == 1028:
                print(combo, remaining_numbers)
                valid_combinations.append(combo)

# Print valid combinations
# for combination in valid_combinations:
#     print(combination)
