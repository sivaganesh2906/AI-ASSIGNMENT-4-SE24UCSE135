from csp import CSP, backtracking_search

def print_sudoku(assignment):
    print("--- Task 3: Sudoku Solution ---")
    for r in range(9):
        row = ""
        for c in range(9):
            row += str(assignment[(r, c)]) + " "
            if c == 2 or c == 5:
                row += "| "
        print(row)
        if r == 2 or r == 5:
            print("-" * 21)
    print("-" * 31)

def solve_sudoku():
    variables = [(r, c) for r in range(9) for c in range(9)]
    
    # Initialize domains (1-9)
    # Just an empty board for the example, but can add initial clues here.
    # Let's add a few initial values to make it a real puzzle, or just leave it empty.
    # We will add a simple partially filled sudoku.
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    domains = {}
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0:
                domains[(r, c)] = [puzzle[r][c]]
            else:
                domains[(r, c)] = list(range(1, 10))

    # Identify neighbors constraint map
    neighbors = {v: set() for v in variables}
    for r in range(9):
        for c in range(9):
            # Same row and col
            for i in range(9):
                if i != r: neighbors[(r, c)].add((i, c))
                if i != c: neighbors[(r, c)].add((r, i))
            
            # Same 3x3 block
            br, bc = r // 3 * 3, c // 3 * 3
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    if (i, j) != (r, c):
                        neighbors[(r, c)].add((i, j))
    
    # Turn sets back to lists
    neighbors = {k: list(v) for k, v in neighbors.items()}

    def constraint_fn(var1, val1, var2, val2, assignment):
        return val1 != val2

    csp = CSP(variables, domains, neighbors, constraint_fn)
    solution = backtracking_search(csp)
    
    if solution:
        print_sudoku(solution)
    else:
        print("No Sudoku solution found.")

if __name__ == '__main__':
    solve_sudoku()
