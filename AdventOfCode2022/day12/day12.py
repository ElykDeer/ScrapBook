#!/usr/bin/env python3

start = None
END = None
PUZZLE_INPUT = []
with open("puzzle_input.txt", 'r') as f:
  for y, line in enumerate(f.read().splitlines()):
    result = []
    for x, c in enumerate(line):
      if c == "S":
        start = (x, y)
        result.append(0)
      elif c == "E":
        END = (x, y)
        result.append(25)
      else:
        result.append(ord(c) - ord('a'))
    PUZZLE_INPUT.append(result)
assert(isinstance(start, tuple))
assert(isinstance(END, tuple))


MAX_X = len(PUZZLE_INPUT[0])
MAX_Y = len(PUZZLE_INPUT)
def is_out_of_bounds(position: tuple[int, int]) -> bool:
  x, y = position
  return x < 0 or y < 0 or y >= MAX_Y or x >= MAX_X


def is_climbable(position: tuple[int, int], next_position: tuple[int, int]) -> bool:
  x1, y1 = position
  x2, y2 = next_position
  return PUZZLE_INPUT[y2][x2] <= PUZZLE_INPUT[y1][x1] + 1


def find_paths(position: tuple[int, int], path_to_me: set[tuple[int, int]] = set()) -> list[set[tuple[int, int]]]:
  # Win condition
  if position == END:
    print(f"Found path to end! (length {len(path_to_me)})")
    return [set()]

  paths_to_end = []

  # Recurse
  x, y = position
  for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
    next_position = (x + dx, y + dy)

    # Don't recurse conditions
    if next_position in path_to_me:
      continue
    if is_out_of_bounds(next_position):
      continue
    if not is_climbable(position, next_position):
      continue

    # Get all paths from here to the end
    for path in find_paths(next_position, path_to_me.union([position])):
      paths_to_end.append(path.union([position]))

  return paths_to_end


all_paths = find_paths(start)
print(min([len(path) for path in all_paths]))
