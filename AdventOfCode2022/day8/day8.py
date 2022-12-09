#!/usr/bin/env python3

# Read input
with open("puzzle_input.txt", 'r') as f:
  puzzle_input = [[int(e) for e in line] for line in f.read().splitlines()]

def get_vert_slice(x: int) -> list[int]:
  return [row[x] for row in puzzle_input]

def check(x: int, y: int) -> bool:
  tree_height = puzzle_input[y][x]

  # Left and right slices
  if max(puzzle_input[y][:x]) < tree_height or max(puzzle_input[y][x+1:]) < tree_height:
    return True

  # Up and down slices
  vert_slice = get_vert_slice(x)
  if max(vert_slice[:y]) < tree_height or max(vert_slice[y+1:]) < tree_height:
    return True

  return False

count = 0
for x in range(len(puzzle_input[0])):
  for y in range(len(puzzle_input)):
    if x == 0 or y == 0 or x == len(puzzle_input[0]) - 1 or y == len(puzzle_input) - 1 or check(x, y):
      count += 1
print(f"Part 1: {count}")

def score(x: int, y: int) -> int:
  tree_height = puzzle_input[y][x]

  total_score = 0

  # Left
  score = 0
  for tree in puzzle_input[y][:x][::-1]:
    score += 1
    if tree >= tree_height:
      break
  total_score += score

  # Right
  score = 0
  for tree in puzzle_input[y][x+1:]:
    score += 1
    if tree >= tree_height:
      break
  total_score *= score

  # Up
  score = 0
  vert_slice = get_vert_slice(x)
  for tree in vert_slice[:y][::-1]:
    score += 1
    if tree >= tree_height:
      break
  total_score *= score

  # Down
  score = 0
  for tree in vert_slice[y+1:]:
    score += 1
    if tree >= tree_height:
      break
  total_score *= score

  return total_score

print(f"Part 2: {max([score(x,y) for x in range(len(puzzle_input[0])) for y in range(len(puzzle_input))])}")