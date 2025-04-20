import time
from collections import deque, defaultdict

def load_puzzles(file="sudoku.txt"):
    with open(file, "r") as f:
        return [line.strip() for line in f if len(line.strip()) == 81]

def build_neighbors():
    neighbors = defaultdict(set)
    for i in range(81):
        row, col = divmod(i, 9)
        for j in range(81):
            if i == j:
                continue
            r, c = divmod(j, 9)
            if r == row or c == col or (r // 3 == row // 3 and c // 3 == col // 3):
                neighbors[i].add(j)
    return neighbors

def ac3(domains, neighbors):
    queue = deque((xi, xj) for xi in range(81) for xj in neighbors[xi])
    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    for x in set(domains[xi]):
        if all(x == y for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

def select_unassigned(puzzle, domains):
    return min(
        (i for i in range(81) if puzzle[i] in '0.'),
        key=lambda i: len(domains[i]),
        default=None
    )

def is_valid(puzzle, index, val, neighbors):
    return all(puzzle[n] != val for n in neighbors[index])

def backtrack(puzzle, domains, neighbors):
    if '.' not in puzzle and '0' not in puzzle:
        return puzzle

    idx = select_unassigned(puzzle, domains)
    for val in sorted(domains[idx]):
        if is_valid(puzzle, idx, val, neighbors):
            puzzle_copy = puzzle[:]
            puzzle_copy[idx] = val
            domains_copy = [d.copy() for d in domains]
            result = backtrack(puzzle_copy, domains_copy, neighbors)
            if result:
                return result
    return None

def solve(puzzle_str):
    puzzle = list(puzzle_str)
    domains = [set('123456789') if c in '0.' else {c} for c in puzzle]
    neighbors = build_neighbors()

    if not ac3(domains, neighbors):
        return None

    result = backtrack(puzzle, domains, neighbors)
    return ''.join(result) if result else None

if __name__ == "__main__":
    puzzles = load_puzzles()
    for idx, puzzle in enumerate(puzzles, 1):
        print(f"\nPuzzle #{idx}")
        start = time.time()
        solution = solve(puzzle)
        duration = time.time() - start
        print(solution if solution else "No solution found.")
        print(f"⏱️ Time: {duration:.5f} seconds")
