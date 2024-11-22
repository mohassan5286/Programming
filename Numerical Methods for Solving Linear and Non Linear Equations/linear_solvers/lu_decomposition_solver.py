import numpy as np
import time
import math

from linear_solvers.direct_methods_solver import DirectMethodsSolver


# this function is used to calculate number of significant figures
def sig_figs(x, n):
    # Check if input is an ndarray, apply the function element-wise if so
    if isinstance(x, np.ndarray):
        return np.vectorize(lambda y: sig_figs(y, n))(x)
    else:
        # Check if the desired number of significant figures is valid
        if n <= 0:
            raise ValueError("Number of significant figures must be positive.")
        # Handle the case where the input is zero
        if x == 0:
            return 0.0

        # Use the built-in round function with precision
        # to round the number to the specified number of significant figures
        rounded_x = round(x, -int(np.floor(np.log10(abs(x)))) + n - 1)
        
        # Convert to integer if the result is an integer
        if isinstance(rounded_x, int):
            rounded_x = int(rounded_x)

        return rounded_x

class LuDecompositionSolver(DirectMethodsSolver):

    def __init__(self, type='doolittle', precision=1e-5):
        super().__init__(precision=precision)
        self._type = type

    @staticmethod
    def doolittleDecomposition(A, precision):
        # calculate the starting time
        start_time = time.time()
    
        # A is the augmented matrix
        A = np.array(A)
        
        # get Y vector from the augmented matrix    
        Y = sig_figs(A[:, -1], precision)
    
        # get the coefficient matrix from the augmented matrix
        A_coefficient = sig_figs(A[:, :-1], precision)
    
        # check if the system doesn't have unique solutions
        det_A = np.linalg.det(A_coefficient)
        if det_A == 0:
            return None, None, None, None, None, None
    
        # check if the coefficient matrix is square
        if A_coefficient.shape[0] != A_coefficient.shape[1]:
            return None, None, None, None, None, None
    
        # create steps list
        steps = []
    
        # calculate the one-side dimension of the matrix
        n = A_coefficient.shape[0]
    
        # initialize the lower triangular matrix as an identity matrix
        L = np.eye(n)
    
        # initialize the upper triangular matrix as a matrix of zeros
        U = np.zeros((n, n))
    
        for i in range(n):
            # Implement partial pivoting
            pivot_row = max(range(i, n), key=lambda k: abs(A_coefficient[k][i]))
            A_coefficient[[i, pivot_row]] = A_coefficient[[pivot_row, i]]
            Y[[i, pivot_row]] = Y[[pivot_row, i]]
            steps.append(f"Swap rows {i+1} and {pivot_row+1}")
    
            for j in range(i, n):
                # calculate U[i][j]
                U[i][j] = sig_figs(A_coefficient[i][j] - sum(L[i][k] * U[k][j] for k in range(i)), precision)
                steps.append(f"U{i}{j} = {U[i][j]}")
    
            for j in range(i+1, n):
                # calculate L[j][i]
                divisor = sig_figs(U[i][i], precision)
                L[j][i] = sig_figs((A_coefficient[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / divisor, precision)
                steps.append(f"L{j}{i} = {L[j][i]}")
    
        # AX = Y
        # LU = A    
        # LUX = Y            
        # UX = Z
        # LZ = Y             
        
        # apply forward substitution to get Z
        Z = sig_figs(np.linalg.solve(L, Y), precision)
        for i in range(Z.shape[0]):
            steps.append(f"Z{i} = {Z[i]}")
    
        # apply backward substitution to get X
        X = sig_figs(np.linalg.solve(U, Z), precision)
        for i in range(X.shape[0] - 1, -1, -1):
            steps.append(f"X{i} = {X[i]}")
    
        # calculate the ending time
        end_time = time.time()
        
        # calculate execution time
        Time = end_time - start_time
        
        # calculate error
        A_coefficient_exact = A[:, :-1]
        Y_exact = A[:, -1]
        exact_solution = np.linalg.solve(A_coefficient_exact, Y_exact)
        error = np.linalg.norm(exact_solution - X)
    
        # return Doolittle lower triangular matrix & Doolittle upper triangular matrix & Solutions & time & error & steps
        return L, U, X, Time, error, steps

    @staticmethod
    def croutDecomposition(A, precision):

        # calculate the starting time
        start_time = time.time()

        # A is the augmented matrix 
        
        # get Y vector from the augmented matrix    
        Y = sig_figs(np.array(A)[:, -1], precision)

        # get the coefficient matrix from the augmented matrix
        A_coefficient = sig_figs(np.array(A)[:, :-1], precision)

        # check if the system doesn't have unique solutions
        det_A = np.linalg.det(A_coefficient)
        if det_A == 0:
            return None, None, None, None, None, None

        # check if the coefficient matrix is square
        if A_coefficient.shape[0] != A_coefficient.shape[1]:
            return None, None, None, None, None, None

        # create steps list
        steps = []

        # calculate the one-side dimension of the matrix
        n = A_coefficient.shape[0]
        
        # initialize the lower triangular matrix as a matrix of zeros
        L = np.zeros((n, n))

        # initialize the upper triangular matrix as identity matrix
        U = np.eye(n)

        for i in range(n):
            # Implement partial pivoting
            pivot_row = max(range(i, n), key=lambda k: abs(A_coefficient[k][i]))
            A_coefficient[[i, pivot_row]] = A_coefficient[[pivot_row, i]]
            Y[[i, pivot_row]] = Y[[pivot_row, i]]
            steps.append(f"Swap rows {i+1} and {pivot_row+1}")

            for j in range(n):
                # calculate L[i][j] in case j is equal to 0
                if j == 0:
                    steps.append("L" + str(i) + str(j) + " = " + str(sig_figs(A_coefficient[i][j], precision)))
                    L[i][j] = sig_figs(A_coefficient[i][j], precision)
                    continue

                # calculate U[i][j] in case i is equal to 0 and j is greater than 0
                if i == 0 and j != 0:
                    steps.append("U" + str(i) + str(j) + " = " + str(sig_figs(A_coefficient[i][j] / A_coefficient[0][0], precision)))
                    U[i][j] = sig_figs(A_coefficient[i][j] / A_coefficient[0][0], precision)
                    continue

                # calculate L[i][j] in case i is greater than or equal to j
                if i >= j:
                    sum = 0
                    for k in range(j):
                        sum += sig_figs(L[i][k] * U[k][j], precision)

                    steps.append("L" + str(i) + str(j) + " = " + str(sig_figs(A_coefficient[i][j] - sum, precision)))
                    L[i][j] = sig_figs(A_coefficient[i][j] - sum, precision)

                if j >= i + 1:
                    
                    if (L[i][i] == 0):
                        return None, None, None, None, None, None

                    # calculate U[i][j] in case j is greater than or equal to i
                    sum = 0
                    for k in range(i):
                        sum += sig_figs(L[i][k] * U[k][j], precision)

                    steps.append("U" + str(i) + str(j) + " = " + str(sig_figs(sig_figs((A_coefficient[i][j] - sum), precision) / L[i][i], precision)))
                    U[i][j] = sig_figs(sig_figs((A_coefficient[i][j] - sum), precision) / L[i][i], precision)

        # AX = Y
        # LU = A    
        # LUX = Y            
        # UX = Z
        # LZ = Y             
                    
        # apply forward substitution to get Z
        Z = sig_figs(np.linalg.solve(L, Y), precision)
        for i in range (0, Z.shape[0]):
            steps.append("Z" + str(i) + " = " + str(Z[i]))

        # apply backward substitution to get X
        X = sig_figs(np.linalg.solve(U, Z), precision)                        
        for i in range (X.shape[0] - 1, -1, -1):
            steps.append("X" + str(i) + " = " + str(X[i]))

        # calculate the ending time
        end_time = time.time()
        
        # calculate execution time
        Time = end_time - start_time
        
        # calculate error
        A_coefficient_exact = np.array(A)[:, :-1]
        Y_exact = np.array(A)[:, -1]
        exact_solution = np.linalg.solve(A_coefficient_exact, Y_exact)
        error = np.linalg.norm(exact_solution - X)    
        
        # return Crout lower triangular matrix & Crout upper triangular matrix & Solutions & time & error
        return L, U, X, Time, error, steps
    
    @staticmethod
    def choleskyDecomposition(A, precision):

        # calculate the starting time
        start_time = time.time()

        # A is the augmented matrix 

        # get Y vector from the augmented matrix    
        Y = sig_figs(np.array(A)[:, -1], precision)

        # get the coefficient matrix from the augmented matrix
        A_coefficient = sig_figs(np.array(A)[:, :-1], precision)

        # check if the system doesn't have unique solutions
        det_A = np.linalg.det(A_coefficient)
        if det_A == 0:
            return None, None, None, None, None, None

        # check if the coefficient matrix is not square
        if A_coefficient.shape[0] != A_coefficient.shape[1]:
            return None, None, None, None, None, None

        # check if the coefficient matrix is not symmetric
        is_symmetric = np.array_equal(A_coefficient, A_coefficient.T)
        if not is_symmetric:
            return None, None, None, None, None, None
        
        # check if the coefficient matrix contains NaN or Inf values
        if np.any(np.isnan(A_coefficient)) or np.any(np.isinf(A_coefficient)):
            return None, None, None, None, None, None

        # create steps list
        steps = []

        # calculate the one-side dimension of the coefficient matrix
        n = A_coefficient.shape[0]

        # initialize the lower triangular matrix as a matrix of zeros
        L = np.zeros((n, n))

        for i in range(n):
            # Implement partial pivoting
            pivot_row = max(range(i, n), key=lambda k: abs(A_coefficient[k, i]))
            A_coefficient[[i, pivot_row]] = A_coefficient[[pivot_row, i]]
            Y[[i, pivot_row]] = Y[[pivot_row, i]]
            steps.append(f"Swap rows {i+1} and {pivot_row+1}")

            for j in range(i+1):
                # calculate L[i][i] in case of the two indices are equal            
                if i == j:
                    sum = 0
                    for k in range(j):
                        sum += sig_figs(L[j, k] ** 2, precision)    

                    steps.append("L" + str(i) + str(j) + " = " + str(sig_figs(math.sqrt(sig_figs((A_coefficient[j, j] - sum), precision)), precision)))
                    L[j, j] = sig_figs(math.sqrt(sig_figs((A_coefficient[j, j] - sum), precision)), precision)
                
                else:
                    # handle error of division by zero (zero pivot)
                    if L[j, j] == 0:
                        return None, None, None, None, None, None

                    # calculate L[i][j] in case of the two indices are not equal
                    sum = 0
                    for k in range(j):
                        sum += sig_figs(L[i, k] * L[j, k], precision)

                    steps.append("L" + str(i) + str(j) + " = " + str(sig_figs(sig_figs((A_coefficient[i, j] - sum), precision) / L[j, j], precision)))
                    L[i, j] = sig_figs(sig_figs((A_coefficient[i, j] - sum), precision) / L[j, j], precision)

        # AX  = Y
        # LU  = A    
        # LUX = Y            
        # UX  = Z
        # LZ  = Y             
        
        # apply forward substitution to get Z
        Z = sig_figs(np.linalg.solve(L, Y), precision)
        for i in range (0, Z.shape[0]):
            steps.append("Z" + str(i) + " = " + str(Z[i]))

        # apply backward substitution to get X
        X = sig_figs(np.linalg.solve(L.T, Z), precision)                        
        for i in range (X.shape[0] - 1, -1, -1):
            steps.append("X" + str(i) + " = " + str(X[i]))

        # calculate ending time
        end_time = time.time()

        # calculate execution time
        Time = end_time - start_time 
        
        # calculate error
        A_coefficient_exact = np.array(A)[:, :-1]
        Y_exact = np.array(A)[:, -1]
        exact_solution = np.linalg.solve(A_coefficient_exact, Y_exact)
        error = np.linalg.norm(exact_solution - X)    

        # return Cholesky lower triangular matrix & Cholesky upper triangular matrix & Solutions & time & error & steps
        return L, L.T, X, Time, error, steps

    def solve(self, system_matrix, type,  precision):

        if(type != None):
            self._type = type
        if(precision != None):
            self._precision = precision
        self._system_matrix = system_matrix

        #SOLVE EQUATIONS HERE
        if(self._type == 'Doolittle Form'):
            return  LuDecompositionSolver.doolittleDecomposition(self._system_matrix, self._precision)
        elif(self._type == 'Crout Form'):
            return LuDecompositionSolver.croutDecomposition(self._system_matrix, self._precision)
        elif(self._type == 'Cholesky Form'):
           return  LuDecompositionSolver.choleskyDecomposition(self._system_matrix, self._precision)
        else:
            return None, None, None, None, None, None

        

