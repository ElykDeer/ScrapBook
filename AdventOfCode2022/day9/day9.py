#!/usr/bin/env python3

from time import sleep

# Read input
with open("puzzle_input.txt", 'r') as f:
  puzzle_input = []
  for line in f.read().splitlines():
    direction, count = line.split(' ')
    count = int(count)

    # Fuck it, unroll the instructions
    for _ in range(count):
      if direction == 'R':
        puzzle_input.append((1,0))
      elif direction == 'L':
        puzzle_input.append((-1,0))
      elif direction == 'U':
        puzzle_input.append((0,-1))
      elif direction == 'D':
        puzzle_input.append((0,1))

tail_positions = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
tracked_tail_positions = set()
for inst, (dx,dy) in enumerate(puzzle_input):
  # if inst == 20:
  #   break
  print(tail_positions)
  # for y in range(221):
  #   for x in range(376):
  for y in range(-15, 15):
    for x in range(-15, 15):
      if (x,y) in tail_positions:
        print("#", end="")
      else:
        print(".", end="")
    print()
  print("\n\n\n")
  sleep(1.0/30.0)

  # Move head
  hx, hy = tail_positions[0]
  prev = tail_positions[0]
  tail_positions[0] = (hx + dx, hy + dy)

  # Check if tail needs to move
  for i, (tx, ty) in enumerate(tail_positions[1:], 1):
    hx, hy = tail_positions[i-1]
    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
      tail_positions[i], prev = prev, tail_positions[i]

  tracked_tail_positions.add(tail_positions[-1])

# print(min([x for (x,y) in tracked_tail_positions]))
# print(max([x for (x,y) in tracked_tail_positions]))
# print(min([y for (x,y) in tracked_tail_positions]))
# print(max([y for (x,y) in tracked_tail_positions]))

tracked_tail_positions.add(tail_positions[-1])
print(f"Part 1: {len(tracked_tail_positions)}")
