import time
from collections import deque

def read_puzzles(filename="sudoku.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if len(line.strip()) == 81]

def make_arcs():
    arcs = []
    for i in range(81):
        row, col = divmod(i, 9)
        for j in range(81):
            if i != j:
                r2, c2 = divmod(j, 9)
                same_row = row == r2
                same_col = col == c2
                same_box = (row // 3 == r2 // 3) and (col // 3 == c2 // 3)
                if same_row or same_col or same_box:
                    arcs.append((i, j))
    return arcs

def ac3(domains):
    queue = deque(make_arcs())
    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk, _ in make_arcs():
                if _ == xi:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    for x in list(domains[xi]):
        if all(x == y for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

def is_consistent(index, value, assignment):
    row, col = divmod(index, 9)
    for i in range(81):
        if assignment[i] == value:
            r, c = divmod(i, 9)
            same_row = r == row
            same_col = c == col
            same_box = (r // 3 == row // 3) and (c // 3 == col // 3)
            if same_row or same_col or same_box:
                return False
    return True

def backtrack(assignment, domains):
    if '.' not in assignment:
        return assignment
    index = assignment.index('.')
    for value in sorted(domains[index]):
        if is_consistent(index, value, assignment):
            new_assignment = assignment[:]
            new_assignment[index] = value
            result = backtrack(new_assignment, domains)
            if result:
                return result
    return None

def solve_sudoku(puzzle):
    assignment = list(puzzle)
    domains = [set('123456789') if c in '0.' else {c} for c in assignment]
    if not ac3(domains):
        return None
    return ''.join(backtrack(assignment, domains))

if __name__ == "__main__":
    puzzles = read_puzzles()
    for idx, p in enumerate(puzzles, 1):
        print(f"\nPuzzle #{idx}")
        start = time.time()
        solution = solve_sudoku(p)
        end = time.time()
        print(solution if solution else "No solution found.")
        print(f"Time: {end - start:.5f} seconds")
