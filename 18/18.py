import re  # search (test if string matches regex), findall, sub (replace), finditer
from collections import defaultdict, deque, Counter, OrderedDict

from sortedcontainers import SortedDict, SortedSet, SortedList
import heapq
import bisect
from itertools import combinations, combinations_with_replacement, permutations, product
import math
from copy import deepcopy
import numpy as np
from sympy.ntheory.modular import crt
from functools import cmp_to_key

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import ints, words, flatten, floats


filename = "./input.txt" if len(sys.argv) < 2 else sys.argv[1]
lines = [line.strip() for line in open(filename, "r").readlines()]


corners_at_height = defaultdict(list)


def add_corner(pos, prevdir, dir):
    global corners_at_height
    i, j = pos
    if (prevdir, dir) in (("U", "R"), ("L", "D")):
        corners_at_height[i].append((j, 1))
    if (prevdir, dir) in (("D", "R"), ("L", "U")):
        corners_at_height[i].append((j, 2))
    if (prevdir, dir) in (("R", "U"), ("D", "L")):
        corners_at_height[i].append((j, 3))
    if (prevdir, dir) in (("R", "D"), ("U", "L")):
        corners_at_height[i].append((j, 4))


ans = 0


dirs1 = []
dirs2 = []

for line in lines:
    dir, n, color = line.split()
    color = color[2:-1]
    n = int(n)
    dir2 = ["R", "D", "L", "U"][int(color[-1])]
    n2 = int(color[:-1], 16)
    dirs1.append((dir, n))
    dirs2.append((dir2, n2))

pos = (0, 0)
edge = set()
prevdir = None

for dir, n in dirs1:
    di, dj = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}[dir]
    add_corner(pos, prevdir, dir)
    i, j = pos
    pos = (i + n * di, j + n * dj)
    prevdir = dir
dir = dirs2[0][0]
add_corner(pos, prevdir, dir)


def count_at_height(corners, vlines):
    xcorners = [c[0] for c in corners]
    new_vlines = [line for line in vlines if line not in xcorners]
    new_corners = deepcopy(corners)
    for line in new_vlines:
        new_corners.append((line, 0))
    new_corners.sort()
    print(new_corners)
    interior = 0

    i = 0
    inside = False
    while i < len(new_corners) - 1:
        print("inside", inside, i)
        cj, ctype = new_corners[i]
        tj, ttype = new_corners[i + 1]
        # line
        if ctype == 0:
            inside = not inside
            if inside:
                interior += tj - cj + 1
        else:
            if ttype != 0:
                if (ctype, ttype) in ((1, 3), (2, 4)):
                    inside = not inside
                interior += tj - cj + 1
            elif inside:
                interior += tj - cj + 1

        i += 1

    return interior


CS = sorted(corners_at_height.items())

vlines = []

for h, corners in CS:
    lc = count_at_height(corners, vlines)
    for j, ctype in corners:
        if ctype in (1, 4):
            vlines.append(j)
        elif ctype in (2, 3):
            vlines.remove(j)
    vlines.sort()
    inside = False
    n_in = 1
    assert len(vlines) % 2 == 0
    for i in range(len(vlines) // 2):
        n_in += vlines[2 * i + 1] - vlines[2 * i]
    print("line", lc)
    # print("inside", n_in)
    print()
    ans += n_in * (1)

exit()
size = 50
grid = [["."] * size for i in range(size)]
added = set()


print(corners_at_height)
for i in range(top, bottom + 1):
    inside = False
    j = left
    while j < right:
        if corner(i, j):
            c1 = corner(i, j)
            assert c1 not in (3, 4)
            j += 1
            while not corner(i, j):
                j += 1
            c2 = corner(i, j)
            assert c2 in (3, 4)
            if c1 == 1 and c2 == 3 or c1 == 2 and c2 == 4:
                inside = not inside
        elif (i, j) in edge:
            inside = not inside

        if inside and (i, j) not in edge:
            added.add((i, j))
            ans += 1
        j += 1
print(len(added) + len(edge))
# for i, j in edge:
#     grid[i][j] = "#"
# for i, j in added:
#     grid[i][j] = "$"
# edge |= added
# for line in grid[:20]:
#     print("".join(line))
