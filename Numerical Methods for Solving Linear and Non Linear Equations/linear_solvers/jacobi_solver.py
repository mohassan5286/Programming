if __name__ == "__main__":
    from iterative_methods_solver import IterativeSolver
else:
    from linear_solvers.iterative_methods_solver import IterativeSolver

import numpy as np
class JacobiSolver(IterativeSolver):
    
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



def jacobi(coefficients, constants, initial_guess, max_iterations, sig_figures, abs_relative_error):
    num_equations = len(coefficients)
    num_variables = len(coefficients[0])
    
    # Convert the input lists to numpy arrays
    A = np.array(coefficients)
    b = np.array(constants)
    x = np.array(initial_guess)
    
    
    # Initialize the iteration counter
    iteration = 0

    result = 0
    
    # Create a list to store the values of x for each iteration
    x_values = []
    
    # Iterate until the maximum number of iterations is reached or the desired accuracy is achieved
    while iteration < max_iterations:
        x_prev = np.copy(x)
        x_new = np.zeros_like(x)
        
        # Perform one iteration of the Jacobi method
        for i in range(num_equations):
            sigma = 0
            for j in range(num_variables):
                if j != i:
                    sigma += A[i][j] * x_prev[j]
            x_new[i] = (b[i] - sigma) / A[i][i]
        
        # Round the values of x to the specified number of significant figures for each iteration
        rounded_x = sig_figs(x_new, sig_figures)
        
        # Append the current values of x to the list
        x_values.append(rounded_x.copy())
        
        # Calculate the absolute relative error
        error = np.abs((x_new - x_prev) / x_new)
        
        # Check if the desired accuracy is achieved
        if np.max(error) < abs_relative_error:
            print(f"Jacobi method converged in {iteration+1} iterations.")
            break
        
        # Update x with the new values
        x = np.copy(x_new)
        
        # Increment the iteration counter
        iteration += 1
    
    # Check if the desired accuracy is not achieved within the given number of iterations
    if iteration == max_iterations:
        result = "Jacobi method did not converge within the specified iterations."
    else:
        result = "Jacobi method converges within the specified iterations."
    
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

    # Solve the system using Jacobi method
    x_values = jacobi(coefficients, constants, initial_guess, max_iterations, sig_figures, abs_relative_error)
    
    # Print the rounded values of x for each iteration
    for i, x in enumerate(x_values):
        rounded_x = sig_figs(x, sig_figures)
        print(f"Iteration {i+1}: {rounded_x}")

