class CSP:
    def __init__(self, variables, domains, neighbors, constraint_function):
        """
        variables: A list of variables.
        domains: A dict mapping variables to lists of possible values.
        neighbors: A dict mapping variables to lists of neighboring variables.
        constraint_function: A function f(var1, val1, var2, val2) that returns True if the assignment is valid.
        """
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint_function = constraint_function
        
    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        count = 0
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraint_function(var, val, neighbor, assignment[neighbor], assignment):
                    count += 1
        # Also check general constraints if the user defined a specific method or just handle it inside constraint_function
        return count


def num_legal_values(csp, var, assignment):
    if not csp.domains[var]:
        return 0
    count = 0
    for val in csp.domains[var]:
        if csp.nconflicts(var, val, assignment) == 0:
            count += 1
    return count


def select_unassigned_variable(assignment, csp):
    # Minimum Remaining Values (MRV) heuristic
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda var: num_legal_values(csp, var, assignment))


def order_domain_values(var, assignment, csp):
    return csp.domains[var]  # Returning original order


def backtracking_search(csp):
    return backtrack({}, csp)


def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables):
        return assignment
    
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if csp.nconflicts(var, value, assignment) == 0:
            csp.assign(var, value, assignment)
            result = backtrack(assignment, csp)
            if result is not None:
                return result
            csp.unassign(var, assignment)
    return None
