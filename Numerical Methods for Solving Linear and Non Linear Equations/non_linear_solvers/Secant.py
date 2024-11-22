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
        if x == np.inf or x == -np.inf:
            return x

        # Use the built-in round function with precision
        rounded_x = round(x, -int(np.floor(np.log10(abs(x)))) + n - 1)
        
        # Convert to integer if the result is an integer
        if isinstance(rounded_x, int):
            rounded_x = int(rounded_x)

        return rounded_x

def secant_method(func, x_prev, x_curr, es, max_itr, precision, single_step_mode=False):
    iteration_data = []  # Initialize list to store iteration data

    iter_count = 0  # Keep track of the number of iterations
    ea = np.inf  # Initialize ea to infinity before the loop

    num_iter_used = 0
    while True:
        num_iter_used += 1

        if x_curr == x_prev:
            relative_error = 0.0
            break

        f_prev = func(x_prev)
        f_curr = func(x_curr)

        print("f_prev:", f_prev, "f_curr:", f_curr)
        if f_curr - f_prev == 0:
            print("Division by zero encountered. Cannot continue the iteration.")
            return None, iteration_data, num_iter_used

        x_next = x_curr - (f_curr * (x_curr - x_prev)) / (f_curr - f_prev)
        print("x_next:", x_next)
        if x_next != 0:
            ea = abs((x_next - x_curr) / x_next) * 100  # Approximate relative error

        iter_count += 1  # Increment iteration count

        x_prev = sig_figs(x_prev, precision)
        x_curr = sig_figs(x_curr, precision)
        x_next = sig_figs(x_next, precision)
        ea = sig_figs(ea, precision)

        iteration_data.append([iter_count, x_prev, x_curr, x_next, ea])  # Store iteration data

        if single_step_mode:  # Check if single-step mode is enabled
            print("Iteration:", iter_count)
            print("x_prev:", x_prev)
            print("x_curr:", x_curr)
            print("x_next:", x_next)
            print("ea:", ea)

            if ea <= es or iter_count >= max_itr:
                if ea <= es:
                    print("Converged to the root:", x_next)
                else:
                    print("Did not converge within the specified error tolerance.")
                break  # Exit the loop if convergence criteria are met

        if ea <= es or iter_count >= max_itr:
            if ea <= es:
                print("Converged to the root:", x_next)
            else:
                print("Did not converge within the specified error tolerance.")
            break  # Exit the loop if convergence criteria are met

        x_prev = x_curr
        x_curr = x_next

    print("Final relative error:", ea, "%")  # Print the final relative error
    return x_next, iteration_data, num_iter_used  # Return the result and iteration data as a tuple

if __name__ == "__main__":
    # Example usage
    func_str = input("Enter the function (e.g., 'cos(x) - 2*x - 5'): ")
    x_prev = float(input("Enter the initial guess x_i-1: "))
    x_curr = float(input("Enter the initial guess x_i: "))

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
        func_lambda = sp.lambdify(x, func, 'numpy')  # Create a lambda function for numerical evaluation
        result, iteration_data = secant_method(func_lambda, x_prev, x_curr, es, max_itr, precision, single_step_mode)
        actresult = sig_figs(result, precision)

        # Get the values from the last row of the iteration data
        x_prev_last, x_curr_last, x_next_last, ea_last = iteration_data[-1]

        if result is not None:
            print("Final result:", actresult)
    except (ValueError, TypeError, SyntaxError) as e:
        print("An error occurred:", e)
