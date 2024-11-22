import sympy as sp
from sympy import sin, cos, tan, exp, log, diff,integrate, I, pi, sqrt, Matrix, Eq, Function
from sympy.abc import x, y, z, t, a, b, c, d, e, f, g, h, k, m, n
import numpy as np
import time


# import numpy as np


class Step:
    x0=0
    x1=0
    f_x=0
    f_d=0
    error=0
     
    def __init__(self, x0,x1,f_x,f_d,error):
        self.x0 = x0
        self.x1 = x1
        self.f_x = f_x
        self.f_d = f_d
        self.error = error

    def getStep(self):
        return self.x0, self.x1,self.f_x,self.f_d, self.error



class Raphson_newton:
    listOfSteps=[]     
    tol = 1e-5
    maxiter = 50
    precision=5
    time_taken=0
    convegence=True
    
    def __init__(self, f, x0, tol, maxiter, precision):
        self.f = f
        self.x0 = x0
        self.tol = tol
        self.maxiter = maxiter
        self.precision=precision
        self.listOfSteps = []

    def formatFloat(self,number): 
        if number==0:
            return 0.0 # or any default value you prefer
        else:
            return format(number, f'.{self.precision}g')

    def solve(self):
        start_time = time.time()

        x = sp.symbols('x')
        f_prime = sp.diff(self.f, x)
        x0=self.formatFloat(self.x0)
        print(f_prime)
        num_iter_used = 0
        for i in range(self.maxiter):
            num_iter_used += 1
            print("Iteration ", num_iter_used)
            divider=f_prime.subs(x, self.x0)
            if divider==0:
                print("Error: division by zero")
                return None
            x1 = self.formatFloat(
                self.x0 - (self.f.subs(x, self.x0) / divider))
           
            x1 = float(x1)
            if abs(x1 - self.x0) < self.tol:
                print("The solution is ", x1)
                break
            if i == self.maxiter - 1 and (abs(self.listOfSteps[-1].error) < abs(x1 - self.x0)):
                print("the solution is diverge ")
                self.convegence = False
                break
            if i==self.maxiter-1:
                print("Maximum number of iterations exceeded")
                break

            
            # Fixing presion for the rest
            tempF = float(self.formatFloat(float(self.f.subs(x, self.x0))))
            tempFPrime = float(self.formatFloat(float(f_prime.subs(x, self.x0))))
            Ea = float(self.formatFloat(abs(x1 - self.x0)))


            # create a step object and add it to the list of steps
            step = Step(self.x0, x1, tempF,
                        tempFPrime, Ea)
            self.listOfSteps.append(step)


            #assign x0 with the value x1 to become the previos value for next iterations 
            self.x0 = x1
            end = time.time()
            self.time_taken = end - start_time
        return x1, num_iter_used
    



# x=sp.symbols('x')
# f = 5*x**2 - 2*8+2
# x0 = -95468
# tol = 1e-5
# maxiter = 200
# precision=5
# x0=float(x0)
# newton = Raphson_newton(f, x0, tol, maxiter, precision)
# newton.solve()

# #print time_taken
# print("Time taken: ", newton.time_taken)

# # print as table
# print("x0\t\t x1\t\t f(x)\t\t f'(x)\t\t error")
# for step in newton.listOfSteps:
#     print(f"{step.x0}\t\t {step.x1}\t\t {step.f_x}\t\t {step.f_d}\t\t {step.error}")


    
