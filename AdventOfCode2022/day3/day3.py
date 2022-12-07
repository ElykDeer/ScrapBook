#!/usr/bin/env python3

import string

with open("puzzle_input.txt", 'r') as f:
  puzzle_input = f.read().splitlines()

total = 0
for rucksack_contents in puzzle_input:
  items = len(rucksack_contents)
  compartment_1 = rucksack_contents[:items//2]
  compartment_2 = rucksack_contents[items//2:]

  element_in_both = set(compartment_1) & set(compartment_2)
  assert(len(element_in_both) == 1)
  element_in_both = list(element_in_both)[0]

  total += (string.ascii_lowercase + string.ascii_uppercase).index(element_in_both) + 1
print(f"Part 1: {total}")

total = 0
for i in range(2, len(puzzle_input), 3):
  element_in_all = list(set(puzzle_input[i]) & set(puzzle_input[i-1]) & set(puzzle_input[i-2]))[0]
  total += (string.ascii_lowercase + string.ascii_uppercase).index(element_in_all) + 1
print(f"Part 2: {total}")