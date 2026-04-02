from csp import CSP, backtracking_search

def australia_map_coloring():
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colors = ['Red', 'Green', 'Blue']
    domains = {var: colors[:] for var in variables}
    
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }

    def constraint_fn(var1, val1, var2, val2, assignment):
        return val1 != val2

    csp = CSP(variables, domains, neighbors, constraint_fn)
    solution = backtracking_search(csp)
    
    print("--- Task 1: Australia Map Coloring ---")
    if solution:
        for var in variables:
            print(f"{var}: {solution[var]}")
    else:
        print("No solution found.")
    print("-" * 38)

if __name__ == '__main__':
    australia_map_coloring()
