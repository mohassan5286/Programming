class IterativeSolver:
    def __init__(self, abs_relative_error=None, max_iterations=300):
        
        self._system_matrix = None
        self._rhs_vector = None
        self._initial_guess = None

        self._abs_relative_error = abs_relative_error
        self._max_iterations = max_iterations

    def solve(self, system_matrix, rhs_vector, initial_guess, tolerance, max_iterations):
        
        raise NotImplementedError("Must implement this method")

