from ortools.sat.python import cp_model
import time

def make_board(s):
    if len(s) != 81 or not all(c in '.123456789' for c in s):
        raise ValueError("Invalid puzzle string")
    return [[int(c) if c != '.' else 0 for c in s[i*9:(i+1)*9]] for i in range(9)]

def board_to_string(board):
    """Convert a 9x9 grid to an 81-character string."""
    if board is None:
        return "No solution"
    return ''.join(str(cell) for row in board for cell in row)

def solve_sudoku(puzzle):
    """Solve the puzzle using OR-Tools CP-SAT and return the solution grid and elapsed time."""
    start = time.time()
    initial_grid = make_board(puzzle)
    model = cp_model.CpModel()
    cell_size = 3
    line_size = cell_size**2
    line = list(range(0, line_size))
    cell = list(range(0, cell_size))
    grid = {}
    for i in line:
        for j in line:
            grid[(i, j)] = model.new_int_var(1, line_size, f"grid {i} {j}")
    for i in line:
        model.add_all_different(grid[(i, j)] for j in line)
    for j in line:
        model.add_all_different(grid[(i, j)] for i in line)
    for i in cell:
        for j in cell:
            one_cell = []
            for di in cell:
                for dj in cell:
                    one_cell.append(grid[(i * cell_size + di, j * cell_size + dj)])
            model.add_all_different(one_cell)
    for i in line:
        for j in line:
            if initial_grid[i][j]:
                model.add(grid[(i, j)] == initial_grid[i][j])
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    elapsed = time.time() - start
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [[0] * 9 for _ in range(9)]
        for i in line:
            for j in line:
                solution[i][j] = int(solver.value(grid[(i, j)]))
        return solution, elapsed
    return None, elapsed

try:
    with open('sudoku.txt', 'r') as f:
        puzzles = [line.strip() for line in f]
    for idx, puzzle in enumerate(puzzles, 1):
        print(f"\n--- Puzzle {idx} ---")
        print(f"Puzzle string: {puzzle}")
        print("Solving...")
        solution, elapsed = solve_sudoku(puzzle)
        print(f"Solution: {board_to_string(solution)}")
        print(f"Total Time: {elapsed:.5f}s")
except FileNotFoundError:
    print("Error: sudoku.txt not found")
except ValueError as e:
    print(f"Error: {e}")
