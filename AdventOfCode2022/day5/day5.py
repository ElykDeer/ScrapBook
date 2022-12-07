#!/usr/bin/env python3

# Read input
with open("puzzle_input.txt", 'r') as f:
  puzzle_input = f.read()

# Split initial state from state machine
starting_layout = puzzle_input.split("\n\n")[0]
instructions = puzzle_input.split("\n\n")[1].splitlines()

# Parse stacks in to usable data
print("Initial State:")
stacks = [[]] + [[element for element in list(line[1:]) if element != ' '] for line in zip(*starting_layout.splitlines()[::-1]) if line[0] != ' ']
for stack in stacks:
  print(stack)
print()

# Run state machine
for instruction in instructions:
  count = int(instruction.split(' ')[1])
  source = int(instruction.split(' ')[3])
  dest = int(instruction.split(' ')[5])

  move = stacks[source][-count:][::-1] # Part 1
  # move = stacks[source][-count:] # Part 2

  stacks[source] = stacks[source][:-count]
  stacks[dest] += move

print("Final State:")
for stack in stacks:
  print(stack)
print()

for stack in stacks[1:]:
  print(stack[-1], end='')
print()
