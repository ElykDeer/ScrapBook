#!/usr/bin/env python3

import requests
from collections import Counter

file = open("../cookie.txt", "r")
cookie = dict(session=file.read().strip())

r = requests.get('https://adventofcode.com/2024/day/1/input', cookies=cookie)

# Part 1
left, right = map(sorted, zip(*[map(int, line.split()) for line in r.text.splitlines()]))
distance = sum(abs(l - r) for l, r in zip(left, right))
print(distance)

# Part 2
# Trying to minimize to O(n) for just part two, so I'm starting over without the sort
left_count, right_count = map(Counter, zip(*[map(int, line.split()) for line in r.text.splitlines()]))
score = sum(val*freq*right_count.get(val, 0) for val, freq in left_count.items())
print(score)
