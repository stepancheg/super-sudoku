#!/usr/bin/env python3

# Z3 solution of Miracle Sudoku
# https://www.theguardian.com/science/2020/may/18/can-you-solve-it-sudoku-as-spectator-sport-is-unlikely-lockdown-hit

import z3

DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

sudoku = [[z3.Int(f"{column}_{row}") for row in range(9)] for column in range(9)]

s = z3.Solver()
for row in sudoku:
    for v in row:
        # Variables only contain digits
        s.add(z3.Or([v == d for d in DIGITS]))

for i in range(9):
    # Each row and column contains distinct values
    s.add(z3.Distinct([sudoku[i][j] for j in range(9)]))
    s.add(z3.Distinct([sudoku[j][i] for j in range(9)]))

# Each of nine big squares should have distinct digits
for i in [0, 3, 6]:
    for j in [0, 3, 6]:
        s.add(z3.Distinct([sudoku[i + k][j + l] for k in range(3) for l in range(3)]))


def is_valid_index(i):
    return i in range(9)


# Eight neighbours are not equal
for i in range(9):
    for j in range(9):
        for i1 in [i - 1, i + 1]:
            for j1 in [j - 1, j + 1]:
                if is_valid_index(i1) and is_valid_index(j1):
                    # Only checking diagonal neighbours because same row/col
                    # neighbours are already excluded by row/col distinct check
                    s.add(sudoku[i][j] != sudoku[i1][j1])


def is_knight_move(i: int, j: int, i1: int, j1: int) -> bool:
    di = abs(i - i1)
    dj = abs(j - j1)
    return (di, dj) in [(1, 2), (2, 1)]


assert is_knight_move(3, 7, 4, 5)
assert is_knight_move(3, 7, 1, 8)

# Knights are not equal
for i in range(9):
    for j in range(9):
        for i1 in [i - 2, i - 1, i + 1, i + 2]:
            for j1 in [j - 1, j - 2, j + 1, j + 2]:
                if not is_valid_index(i1) or not is_valid_index(j1):
                    continue
                if not is_knight_move(i, j, i1, j1):
                    continue
                s.add(sudoku[i][j] != sudoku[i1][j1])


def is_neighbour(i, j, i1, j1):
    if not is_valid_index(i1) or not is_valid_index(j1):
        return False
    di = abs(i - i1)
    dj = abs(j - j1)
    return (di, dj) in [(0, 1), (1, 0)]


assert is_neighbour(3, 6, 3, 5)
assert is_neighbour(3, 6, 3, 7)
assert is_neighbour(3, 6, 4, 6)
assert is_neighbour(3, 6, 2, 6)
assert not is_neighbour(3, 6, 2, 5)

# Next must not be +-1
for i in range(9):
    for j in range(9):
        for i1 in [i - 1, i, i + 1]:
            for j1 in [j - 1, j, j + 1]:
                if is_neighbour(i, j, i1, j1):
                    s.add(sudoku[i][j] - sudoku[i1][j1] != 1)
                    s.add(sudoku[i][j] - sudoku[i1][j1] != -1)

s.add(sudoku[4][2] == 1)
s.add(sudoku[5][6] == 2)

while s.check() == z3.sat:
    print("Found")

    model = s.model()

    for row in range(9):
        print(" ".join([str(model[sudoku[row][column]]) for column in range(9)]))

    # Exclude current solution to find the next one
    s.add(
        z3.Or([sudoku[i][j] != model[sudoku[i][j]] for i in range(9) for j in range(9)])
    )

print("End")

if __name__ == "__main__":
    pass

# vim: set ts=4 sw=4 et:
