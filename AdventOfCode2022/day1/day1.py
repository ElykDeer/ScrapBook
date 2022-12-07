#!/usr/bin/env python3

with open("puzzle_input.txt", 'r') as f:
  puzzle_input = f.read().split('\n\n')

elf_cals = [sum([int(cals) for cals in elf_cals.split('\n')]) for elf_cals in puzzle_input]

print(f"Max cals: {max(elf_cals)}")
print(f"Top three max cals: {sum(sorted(elf_cals)[-3:])}")
