# falsi-position method
import sympy as sp
import time

class Step:
    x_up = 0
    x_lw = 0
    f_x_up = 0
    f_x_lw = 0
    error = 0

    def __init__(self, x_up, x_lw, f_x_up, f_x_lw, error):
        self.x_up = x_up
        self.x_lw = x_lw
        self.f_x_up = f_x_up
        self.f_x_lw = f_x_lw
        self.error = error

    def getStep(self):
        return self.x_up, self.x_lw,self.f_x_up,self.f_x_lw, self.error
    
# falsi-position method
class False_position:
    listOfSteps = []
    tol = 1e-5
    maxiter = 50
    precision = 5
    time_taken = 0
    def __init__(self, f, x_up, x_lw, tol, maxiter, precision):
        self.f = f
        self.x_up = x_up
        self.x_lw = x_lw
        self.tol = tol
        self.maxiter = maxiter
        self.precision = precision
        self.listOfSteps = []
    def formatFloat(self, number):
        return format(number, f'.{self.precision}g')
    # solve method for falsi-position method
    def solve(self):
        start_time = time.time()
        x = sp.symbols('x')
        x_up = float(self.formatFloat(self.x_up))
        x_lw = float(self.formatFloat(self.x_lw))
        print(x_up)
        print(x_lw)

        f_x_up = float(self.formatFloat(float(self.f.subs(x, x_up))))
        f_x_lw = float(self.formatFloat(float(self.f.subs(x, x_lw))))

        if f_x_lw * f_x_up > 0:
            raise Exception("The interval must contain one root where the sign of the function changes around it.")

        num_iter_used = 0
        for i in range(self.maxiter):
            num_iter_used += 1
            f_x_up = float(self.formatFloat(float(self.f.subs(x, x_up))))
            f_x_lw = float(self.formatFloat(float(self.f.subs(x, x_lw))))

            if ((f_x_lw - f_x_up) == 0):
                raise Exception("The interval must contain a root where the sign of the function changes around it.")

            x_r = float(self.formatFloat(((float(x_up) * f_x_lw) - (float(x_lw) * f_x_up)) / (f_x_lw - f_x_up)))
            f_x_r = float(self.formatFloat(float(self.f.subs(x, x_r))))
            if f_x_r == 0:
                print("The solution is ", x_r)
                break
            elif f_x_up * f_x_r < 0:
                x_lw = x_r
            elif f_x_lw * f_x_r < 0:
                x_up = x_r
            else:
                print("The solution is ", x_r)
                break
            x_r = float(self.formatFloat(((float(x_up) * f_x_lw) - (float(x_lw) * f_x_up)) / (f_x_lw - f_x_up)))
            if abs(x_r - x_lw) < self.tol:
                print("The solution is ", x_r)
                break

            ea = float(self.formatFloat(float(abs((x_r - x_lw)/ x_r) * 100)))

            # create a step object and add it to the list of steps
            st = Step(x_up, x_lw, f_x_up, f_x_lw, ea)
            self.listOfSteps.append(st)
            end = time.time()
            self.time_taken = end - start_time
            if i == self.maxiter - 1:
                raise Exception("the solution did not converge within the given parameters")
        return x_r, num_iter_used

# example on falsi-position method
# x = sp.symbols('x')
# f = x ** 2 - 2
# x_up = 2
# x_lw = 1
# tol = 1e-5
# maxiter = 50
# precision = 5
# falsi_position_method = False_position(f, x_up, x_lw, tol, maxiter, precision)
# falsi_position_method.solve()
# # print time_taken
# print("Time taken: ", falsi_position_method.time_taken)
# # print as table
# print("x_up\t\t x_lw\t\t f(x_up)\t\t f(x_lw)\t\t error")
# for step in falsi_position_method.listOfSteps:
#     print(f"{step.x_up}\t\t {step.x_lw}\t\t {step.f_x_up}\t\t\t {step.f_x_lw}\t\t\t {step.error}")