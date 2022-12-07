#!/usr/bin/env python3

with open("puzzle_input.txt", 'r') as f:
  puzzle_input = [line.split(',') for line in f.read().splitlines()]

total_encompassing = 0
total_overlap = 0
for elf_1,elf_2 in puzzle_input:
  elf_1_start, elf_1_end = elf_1.split('-')
  elf_2_start, elf_2_end = elf_2.split('-')

  elf_1_range = set(range(int(elf_1_start), int(elf_1_end)+1))
  elf_2_range = set(range(int(elf_2_start), int(elf_2_end)+1))

  intersection = elf_1_range & elf_2_range
  if len(intersection) == len(elf_1_range) or len(intersection) == len(elf_2_range):
    total_encompassing += 1

  if len(intersection) > 0:
    total_overlap += 1
print(f"Part 1: {total_encompassing}")
print(f"Part 2: {total_overlap}")

