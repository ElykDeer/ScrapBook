#!/usr/bin/env python3

# Read input
with open("puzzle_input.txt", 'r') as f:
  puzzle_input = f.read().splitlines()

file_system = {'/': {}}
cwd = []

index = 0
for instruction in puzzle_input:
  if instruction.startswith('$ '):
    command = instruction[2:].split(' ')[0]
    if command == 'cd':
      arg = instruction[2:].split(' ')[1]
      if arg == '/':
        cwd = ['/']
      elif arg == '..':
        cwd.pop()
      else:
        cwd.append(arg)

  else:
    current_path = file_system
    for path in cwd:
      current_path = current_path[path]

    if instruction.split(' ')[0] == 'dir':
      current_path[instruction.split(' ')[1]] = {}
    else:
      current_path[instruction.split(' ')[1]] = int(instruction.split(' ')[0])

# print(file_system)

tracker = []
def recurse_directory(folder: dict) -> int:
  size = 0
  for value in folder.values():
    if isinstance(value, dict):
      size += recurse_directory(value)
    else:
      size += value
  tracker.append(size)
  return size
recurse_directory(file_system)

total = 0
limit = 100000
for size in tracker:
  if size <= limit:
    total += size
print(f"Part 1: {total}")

disk_size = 70000000
used_disk = max(tracker)
need_disk = 30000000
min_directory_size = need_disk - (disk_size - used_disk)

print(f"Part 2: {min([s for s in tracker if s >= min_directory_size])}")
