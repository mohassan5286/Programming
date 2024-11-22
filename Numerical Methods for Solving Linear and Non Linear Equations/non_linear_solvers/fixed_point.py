import sympy as sp
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



def fixed_point_iteration(func, x0, g, es, max_itr, precision, single_step_mode=False):
    iter_count = 0  # Keep track of the number of iterations
    final_relative_error = None  # Initialize final relative error
    ea = np.inf  # Initialize ea to infinity before the loop
    iteration_data = []  # Initialize an empty list to store iteration data

    num_iter_used = 0
    while True:
        num_iter_used += 1
        x_next = g(x0)
        x_next = sig_figs(x_next, precision)
        if x_next != 0:
            ea = abs((x_next - x0) / x_next) * 100  # Approximate relative error
            ea = sig_figs(ea, precision)
        print("x0:", x0, "x_next:", x_next, "ea:", ea)


        iter_count += 1  # Increment iteration count

        x0 = x_next  # Update x0 with the next value

        iteration_data.append((x0, x_next, ea))  # Store the iteration data

        if single_step_mode:  # Check if single-step mode is enabled
            print(f"Iteration {iter_count}: x0 = {x0}, x_next = {x_next}, ea = {ea}")
            if ea <= es or iter_count >= max_itr:
                final_relative_error = ea  # Store the final relative error
                if ea <= es:
                    print("Converged to the fixed point:", x_next)
                else:
                    print("Did not converge within the specified error tolerance.")
                break  # Exit the loop if convergence criteria are met

        if ea <= es or iter_count >= max_itr:
            if ea <= es:
                final_relative_error = ea  # Store the final relative error
                print("Converged to the fixed point:", x_next)
                break  # Exit the loop if convergence criteria are met
            else:
                raise Exception("The function can't converge within the given paramters")

    print("Final relative error:", ea, "%")  # Print the final relative error
    return sig_figs(iteration_data[-1][1], precision), np.array(iteration_data), num_iter_used  # Return the entire 2D array containing all iteration data


if __name__ == "__main__":
    # Example usage for fixed_point_iteration with user-defined g(x)
    func_str = input("Enter the function (e.g., 'exp(x) - 2'): ")
    x0 = float(input("Enter the initial guess x0: "))
    g_str = input("Enter the function for g(x) (e.g., 'exp(x) - 2 + x'): ")

    try:
        es = float(input("Enter the acceptable relative error (e.g., 0.01 for 1%): "))
        max_itr = int(input("Enter the maximum number of iterations allowed: "))
        precision = int(input("Enter the number of significant figures for the result: "))
    except ValueError:
        print("Invalid input for error or iteration parameters. Please enter valid numbers.")
        exit()

    single_step_mode = input("Enable single-step mode? (y/n): ").lower() == "y"

    try:
        # Define the function using SymPy
        x = sp.symbols('x')
        func = sp.sympify(func_str)  # Parse the function string into a SymPy expression
        g_expr = sp.sympify(g_str)  # Parse the function string for g(x) into a SymPy expression
        g = sp.lambdify(x, g_expr, 'numpy')  # Create a lambda function for numerical evaluation of g(x)
        iteration_data = fixed_point_iteration(func, x0, g, es, max_itr, precision, single_step_mode)
        
        # Get the result from the last row of the iteration data
        result = iteration_data[-1][1]
        actresult = sig_figs(result, precision)
        
        # Get the values from the last row of the iteration data
        x0_last, x_next_last, ea_last = iteration_data[-1]
        
        print("Final result:", actresult)
    except (ValueError, TypeError, SyntaxError) as e:
        print("An error occurred:", e)

