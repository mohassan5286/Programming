import copy
from scipy.linalg import lstsq
import numpy as np
import time 


class GaussElimination:
    EPSILON=1e-8
    flag = True
    list_array=[]
    time_taken=0
    time_start=0
    time_end=0
    status=""
    
    
    def __init__(self):
        self.flag = True
        self.mxEle = []
        self.res = []
        self.array = []
        self.PRESCION=3
        self.status = ""

    def calculate(self, arr):
        self.time_start=time.time()
        self.array = arr
        self.mxEle = [0] * len(self.array)

        for ind_row in range(len(self.array)):
            self.mxEle[ind_row] = abs(self.array[ind_row][0])
            for ind_col in range(2, len(self.array)):
                if abs(self.array[ind_row][ind_col]) > self.mxEle[ind_row]:
                    self.mxEle[ind_row] = abs(self.array[ind_row][ind_col])
        if (self.check() == False):
            self.time_end = time.time()
            self.time_taken = self.time_end - self.time_start
            return

        self.eleminate()
        self.substitute()

      

        print("Results:")
        #apply precision
        for i in range(len(self.res)):
            self.res[i]=self.formatFloat(self.res[i])
        print(self.res)
        print()
        for i in range(len(self.list_array)):
            for j in range(len(self.list_array[i])):
                for k in range(len(self.list_array[i][j])):
                    self.list_array[i][j][k] = self.formatFloat(
                        self.list_array[i][j][k])
        self.time_end = time.time()
        self.time_taken = self.time_end - self.time_start



        # print(self.array)

    def eleminate(self):
        len_ = len(self.array)
        len_ -= 1
        for k in range(len(self.array)):
            self.flag = self.partialPivoting(k)
            if self.flag == False:
                return
            for i in range(k + 1, len(self.array)):
                factor = self.array[i][k] / self.array[k][k]
                for j in range(k, len(self.array)):
                    self.array[i][j] = self.array[i][j] - \
                        factor * self.array[k][j]
                self.array[i][len_ + 1] = self.array[i][len_ + 1] - \
                    factor * self.array[k][len_ + 1]
                self.list_array.append(copy.deepcopy(self.array))

            
          
    def substitute(self):
        len_ = len(self.array)
        self.res = [0] * len_
        len_ -= 1
        self.res[len_] = self.array[len_][len_ + 1] / self.array[len_][len_]


        for ind_row in range(len(self.array) - 2, -1, -1):
            sum_ = 0
            for ind_col in range(ind_row + 1, len(self.array)):
                sum_ = sum_ + self.array[ind_row][ind_col] * self.res[ind_col]
                
            if self.array[ind_row][ind_row] == 0:
                self.res[ind_row] = False
            else:
                self.res[ind_row] = (
                    self.array[ind_row][len_ + 1] - sum_) / self.array[ind_row][ind_row]


    def partialPivoting(self, k):
        len_ = len(self.array) - 1
        p = k
        mx = abs(self.array[k][k] / self.mxEle[k])
        for ind_row in range(k + 1, len(self.array)):
            temp = abs(self.array[ind_row][k] / self.mxEle[ind_row])
            if temp > mx:
                mx = temp
                p = ind_row
        if p != k:
            for ind_col in range(k, len(self.array)):
                temp = self.array[p][ind_col]
                self.array[p][ind_col] = self.array[k][ind_col]
                self.array[k][ind_col] = temp

            tm = self.array[k][len_ + 1]
            self.array[k][len_ + 1] = self.array[p][len_ + 1]
            self.array[p][len_ + 1] = tm

            tm = self.mxEle[p]
            self.mxEle[p] = self.mxEle[k]
            self.mxEle[k] = tm
        if abs(self.array[p][p]) <= self.EPSILON:
            self.flag = False
            return False
        else:
            return True
    def formatFloat(self,number):
        float_number = float(number) 
        return format(float_number, f'.{self.PRESCION}g')
    def check(self):
        arr_cofficient=[]
        arr_cofficient = self.array[:]
        for i in range(len(self.array)):
            arr_cofficient[i] = self.array[i][:-1]
 
        
        # check the rank  for augmented matrix
        rank1 = np.linalg.matrix_rank(self.array)
        print("rank of augmented matrix is: ", rank1)
        # how to calculte the rank in array except the last column

        rank2 = np.linalg.matrix_rank(arr_cofficient)
        print("rank of array except last column is: ", rank2)
        print()
        print()

        if rank1 == rank2:
            if rank1 < len(self.array):
                # print("Infinite solutions  (system is consistent)")
                self.status = "Infinite solutions and one of the solutions is (system is consistent)"
                
                b = np.zeros((len(self.array), 1))
                for i in range(len(self.array)):
                    b[i][0] = self.array[i][-1]
                    
                x=lstsq(arr_cofficient,b)
                
                #copy x to res without change type of res
                
                self.res = [0] * len(self.array)
                for i in range(len(self.array)):
                    self.res[i]=x[0][i][0]

                for i in range(len(self.array)):
                    self.res[i] = self.formatFloat(self.res[i])
                for i in  self.res:
                    print(i)
                return False
                
            else:
                # print("unique solution (system is determined)")
                self.status = "unique solution (system is determined)"
                return True
            
                
        else:
            # print("No solution (system is inconsistent)")
            self.status = "No solution (system is inconsistent)"
            return False



# Example usage:
arr = [[222, 1, -3,5], [4, 2, -654,10], [6, 3, -9,115]]


# gauss_elimination = GaussElimination()
# gauss_elimination.calculate(arr)
# gauss_elimination.res    
#  print all array in array list but new line after every element and after each part of array

#apply precision on list_array


# for i in gauss_elimination.list_array:
#     for j in i:
#         print(j)
#     print()

# print("time taken: ",gauss_elimination.time_taken)
