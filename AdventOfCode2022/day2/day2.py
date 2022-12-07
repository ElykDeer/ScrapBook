#!/usr/bin/env python3

with open("puzzle_input.txt", 'r') as f:
  puzzle_input = [(ord(line.split(' ')[0]) - ord('A') + 1, ord(line.split(' ')[1]) - ord('X') + 1) for line in f.read().splitlines()]

total = 0
for l,r in puzzle_input:
  # Tie
  if l == r:
    total += r + 3

  # Win - this is cursed
  elif r-l == 1 or r-l == -2:
    total += r + 6

  # Lose
  else:
    total += r
print(f"Part 1: {total}")

lookup_table = [3, 1, 2, 3, 1]
total = 0
for l,r in puzzle_input:
  # Lose
  if r == 1:
    total += lookup_table[l-1]

  # Draw
  if r == 2:
    total += l + 3

  # Win
  if r == 3:
    total += lookup_table[l+1] + 6
print("Part 2: {total}")
