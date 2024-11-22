from scipy.linalg import lstsq
import numpy as np
import copy
import random
import time
class GuassJordan:
    EPSILON = 1e-8
    list_array=[]
    array=[]
    flag = True
    res = []
    PRESCION = 3
    time_taken=0
    time_start=0
    time_end=0
    

    def __init__(self):
        self.flag = True
        self.mxEle = []
        self.res = []
        self.array = []

    def calculate(self, arr):
        self.time_start=time.time()
        self.array = arr
        self.mxEle = [0] * len(self.array)
        self.res = [0] * len(self.array)

        for ind_row in range(len(self.array)):
            self.mxEle[ind_row] = abs(self.array[ind_row][0])
            for ind_col in range(2, len(self.array)):
                if abs(self.array[ind_row][ind_col]) > self.mxEle[ind_row]:
                    self.mxEle[ind_row] = abs(self.array[ind_row][ind_col])
        

        if(self.check()==False):
            self.time_end = time.time()
            self.time_taken = self.time_end - self.time_start
            return 
        self.forwardElimination()
        print()
        if(self.flag==False):
            print("No unique solution (system is overdetermined)")
            return
        self.backElimination()
        
        length = len(self.array)
        for i in range(len(self.array)):
            self.res[i] = self.formatFloat(
                self.array[i][length]/self.array[i][i])
        print(self.res)
        print()

     
        for i in range(len(self.list_array)):
            for j in range(len(self.list_array[i])):
                for k in range(len(self.list_array[i][j])):
                    self.list_array[i][j][k] = self.formatFloat(
                        self.list_array[i][j][k])
        self.time_end = time.time()
        self.time_taken = self.time_end - self.time_start
        

    def forwardElimination(self):
        len_ = len(self.array)
        len_ -= 1
        for k in range(len(self.array)):
            self.flag = self.partialPivoting(k)
            if not self.flag:
                return False

            for i in range(k + 1, len(self.array)):
                factor = self.array[i][k] / self.array[k][k]
                # print(factor)
                for j in range(k, len(self.array)):
                    self.array[i][j] = self.array[i][j] - \
                        factor * self.array[k][j]
                self.array[i][len_ + 1] = self.array[i][len_ + 1] - \
                    factor * self.array[k][len_ + 1]
                self.list_array.append(copy.deepcopy(self.array))

        return True

    def backElimination(self):
        len_ = len(self.array)
        len_ -= 1
        for k in range(len_, -1, -1):
            for i in range(k - 1, -1, -1):
                factor = self.array[i][k] / self.array[k][k]
                for j in range(k - 1, len(self.array)):
                    self.array[i][j] = self.array[i][j] - \
                        factor * self.array[k][j]
                self.array[i][len_ + 1] = self.array[i][len_ + 1] - \
                    factor * self.array[k][len_ + 1]
                self.list_array.append(copy.deepcopy(self.array))


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
                print("Infinite solutions  (system is consistent)")
                
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
                print("unique solution (system is determined)")
                return True
            
                
        else:
            print("No solution (system is inconsistent)")
            return False
       

# arr = [[2, 11, -3, 522], [4, 2, -246444, 105], [6, 3, -9, -1551401]]



# gauss_j = GuassJordan()
# gauss_j.calculate(arr)

# #  print all array in array list but new line after every element and after each part of array
# for i in gauss_j.list_array:
#     for j in i:
#         print(j)
#     print()
# print("time taken: ", gauss_j.time_taken)
