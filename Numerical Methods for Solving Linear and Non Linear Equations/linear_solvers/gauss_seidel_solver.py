if __name__ == "__main__":
    from iterative_methods_solver import IterativeSolver
else: from linear_solvers.iterative_methods_solver import IterativeSolver
import numpy as np
class GaussSeidelSolver(IterativeSolver):
    
    def solve(self, system_matrix, rhs_vector, initial_guess, abs_relative_error=None, max_iterations=None, precision=None):
        self._system_matrix = system_matrix
        self._rhs_vector = rhs_vector
        self._initial_guess = initial_guess
        if(abs_relative_error != None):
            self._abs_relative_error = abs_relative_error
        if(max_iterations != None):
            self._max_iterations = max_iterations
        if(precision != None):
            self._precision = precision
        #SOLVE EQUATIONS HERE
            
import numpy as np

def sig_figs(x, n):
    """
    Returns the number or array rounded to n significant figures.

    Args:
        x: A number (int or float) or an ndarray.
        n: An integer representing the desired number of significant figures.

    Returns:
        The number or array rounded to n significant figures.
    """

    if isinstance(x, np.ndarray):
        return np.vectorize(lambda y: sig_figs(y, n))(x)
    else:
        if n <= 0:
            raise ValueError("Number of significant figures must be positive.")
        if x == 0:
            return 0.0

        # Use the built-in round function with precision
        rounded_x = round(x, -int(np.floor(np.log10(abs(x)))) + n - 1)
        
        # Convert to integer if the result is an integer
        if isinstance(rounded_x, int):
            rounded_x = int(rounded_x)

        return rounded_x

def is_diagonally_dominant(coefficients):
    try:
        n = len(coefficients)
        at_least_one_greater = False
        for i in range(n):
            diagonal_value = abs(coefficients[i, i])
            row_sum = np.sum(np.abs(coefficients[i])) - diagonal_value
            if diagonal_value < row_sum:
                return False
            if diagonal_value > row_sum:
                at_least_one_greater = True
        return at_least_one_greater
    except Exception as e:
        print("Error occurred in diagonal dominance check:", e)
        return False

def gauss_seidel(coefficients, constants, initial_guess, max_iterations, sig_figures, abs_relative_error):
    num_equations = len(coefficients)
    num_variables = len(coefficients[0])
    
    # Convert the input lists to numpy arrays
    A = np.array(coefficients)
    b = np.array(constants)
    x = np.array(initial_guess)
    
    # Check if the matrix is diagonally dominant
    is_dominant = is_diagonally_dominant(A)

    result = ""
    
    if is_dominant:
        result = "The matrix is diagonally dominant. Gauss-Seidel method is guaranteed to converge."
    else:
        result = "The matrix is not diagonally dominant. Gauss-Seidel method is not guaranteed to converge."
    
    # Initialize the iteration counter
    iteration = 0
    
    # Create a list to store the values of x for each iteration
    x_values = []
    
    # Iterate until the maximum number of iterations is reached or the desired accuracy is achieved
    while iteration < max_iterations:
        x_prev = np.copy(x)
        
        # Perform one iteration of the Gauss-Seidel method
        for i in range(num_equations):
            sigma = 0
            for j in range(num_variables):
                if j != i:
                    sigma += A[i][j] * x[j]
            x[i] = (b[i] - sigma) / A[i][i]
        
        # Round the values of x to the specified number of significant figures for each iteration
        rounded_x = sig_figs(x, sig_figures)
        
        # Append the current values of x to the list
        x_values.append(rounded_x.copy())
        
        # Calculate the absolute relative error
        error = np.abs((x - x_prev) / x)
        
        # Check if the desired accuracy is achieved
        if np.max(error) < abs_relative_error:
            print(f"Gauss-Seidel method converged in {iteration+1} iterations.")
            break
        
        # Increment the iteration counter
        iteration += 1
    
    # Check if the desired accuracy is not achieved within the given number of iterations
    if iteration == max_iterations:
        print("Gauss-Seidel method did not converge within the specified iterations.")
    
    # Return the list of x values for each iteration
    return x_values, result

if __name__ == "__main__":
    # Get user input
    num_equations = int(input("Enter the number of equations: "))
    num_variables = int(input("Enter the number of variables: "))

    coefficients = []
    constants = []
    initial_guess = []

    print("Enter the coefficients:")
    for i in range(num_equations):
        equation = []
        for j in range(num_variables):
            coefficient = float(input("Enter coefficient A[" + str(i) + "][" + str(j) + "]: "))
            equation.append(coefficient)
        coefficients.append(equation)

    print("Enter the constants:")
    for i in range(num_equations):
        constant = float(input("Enter constant b[" + str(i) + "]: "))
        constants.append(constant)

    print("Enter the initial guess:")
    for i in range(num_variables):
        guess = float(input("Enter initial guess x[" + str(i) + "]: "))
        initial_guess.append(guess)

    max_iterations = int(input("Enter the maximum number of iterations: "))
    sig_figures = int(input("Enter the number of significant figures: "))
    abs_relative_error = float(input("Enter the absolute relative error: "))

    # Solve the system using Gauss-Seidel method
    x_values = gauss_seidel(coefficients, constants, initial_guess, max_iterations, sig_figures, abs_relative_error)
    
    # Print the rounded values of x for each iteration
    for i, x in enumerate(x_values):
        rounded_x = sig_figs(x, sig_figures)
        print(f"Iteration {i+1}: {rounded_x}")
