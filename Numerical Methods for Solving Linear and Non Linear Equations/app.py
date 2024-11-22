import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtWidgets import *
from linear_solvers.gauss_jordan_solver import GuassJordan
from linear_solvers.gauss_seidel_solver import gauss_seidel
from linear_solvers.jacobi_solver import jacobi
from linear_solvers.lu_decomposition_solver import LuDecompositionSolver
from stepWindow import StepWindow
from PyQt5 import QtCore
import time

from linear_solvers.gauss_elimination_solver import GaussElimination
from linear_solvers.gauss_jordan_solver import GuassJordan
# from linear_solvers.lu_decomposition_solver import LuDecompositionSolver
# from linear_solvers.gauss_seidel_solver import GaussSeidelSolver, gauss_seidel_iteration
# from linear_solvers.jacobi_solver import JacobiSolver, jacobi_iteration, is_diagonally_dominant

class MyWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        
        # Attributes
        self.currentMethod = ""
        self.matrixInput = QScrollArea(self)

        self.initialGuessLabel = QLabel("Initial Guess", self)
        self.initialGuessInput = QScrollArea(self)

        self.solutionLabel = QLabel("Solution", self)
        self.solutionOutput = QScrollArea(self)


        
        solver = GaussElimination()

        # Set the size of the main window
        self.setGeometry(100, 100, 1600, 900)  # Set width and height
        
        self.time_taken = 0.0 # Used to display time

        # Set the window title
        self.setWindowTitle("Equations Calculator")

        # Set the window icon
        self.setWindowIcon(QIcon("gui\icons\sigma_icon.png"))
        self.initUI()


        self.steps = [[]] # Used to create the stepWindow

        with open("gui/themes/design1.qss") as f:
            self.setStyleSheet(f.read())

    def stepMode(self, answer, method, sigFig):
        self.ui = StepWindow(answer, method, sigFig)
        self.ui.show()

    def initUI(self):

        #create a label
        label = QLabel('Choose the Method', self)
        label.setObjectName('bigLabel')
        label.setGeometry(25, 160, 400, 100)
        

        # Create a QPushButton
        button = QPushButton('Solve', self)
        button.setGeometry(50, 600, 200, 80)
        button.clicked.connect(lambda :solve())

        # Create a Step Mode Button
        stepModeButton = QPushButton('Step Mode', self)
        stepModeButton.setObjectName(u"smallLabel")
        stepModeButton.setGeometry(500, 610, 200, 60)

# ##############################################################
        # Put the rsult of the solving in variable answer
        answer = [[[1,2,3],[4,5,6], [4,5,6]], [[1,2,3],[4,10,6], [4,5,6]]]
        stepModeButton.clicked.connect(lambda: self.stepMode(self.steps, combo_box.currentText(), int(sigFigInput.text())))

        

        # Create a QComboBox
        combo_box = QComboBox(self)
        combo_box.addItem('Gauss Elimination')
        combo_box.addItem('LU Decomposition')
        combo_box.addItem('Gauss-Jordan Elimination')
        combo_box.addItem('Gauss-Seidel Iteration')
        combo_box.addItem('Jacobi Iteration')
        combo_box.setGeometry(50, 280, 430, 75)  # Adjust the position
        
        combo_box.currentTextChanged.connect(lambda: onComboboxChange(combo_box.currentText()))

        # Change Parameters depend on method
        def onComboboxChange(text):

            noOfIterationLabel.setVisible(False)
            noOfIterationInput.setVisible(False)
            relativeErrorLabel.setVisible(False)
            relativeErrorInput.setVisible(False)
            LUFormComboBox.setVisible(False)
            
            self.initialGuessInput.setVisible(False)
            self.initialGuessLabel.setVisible(False)

            
        
            if text == "Gauss Elimination" or text == 'Gauss-Jordan Elimination':
                pass
            elif text == 'LU Decomposition':
                LUFormComboBox.setVisible(True)
            elif text == 'Gauss-Seidel Iteration' or text == 'Jacobi Iteration':
                noOfIterationLabel.setVisible(True)
                noOfIterationInput.setVisible(True)
                relativeErrorLabel.setVisible(True)
                relativeErrorInput.setVisible(True)
                self.initialGuessLabel.setVisible(True)
                self.initialGuessInput.setVisible(True)

        def LUForm(text):
            pass
            
        # Create input and label for sig fig
        sigFigLabel = QLabel("No of Significant Figures", self)
        sigFigLabel.setGeometry(510, 90, 160, 60)
        sigFigLabel.setObjectName('smallLabel')
        sigFigLabel.setWordWrap(True)
        sigFigLabel.setVisible(True)

        sigFigInput = QLineEdit(self)
        sigFigInput.setGeometry(670, 90, 100, 50)

        # Create input and label for no of iteration
        noOfIterationLabel = QLabel("Number of Iterations", self)
        noOfIterationLabel.setObjectName('smallLabel')
        noOfIterationLabel.setWordWrap(True)
        noOfIterationLabel.setGeometry(510, 160, 160, 60)
        noOfIterationLabel.setVisible(False)

        noOfIterationInput = QLineEdit(self)
        noOfIterationInput.setGeometry(670, 160, 100, 50)
        noOfIterationInput.setVisible(False)

        # Create input and label for relative error
        relativeErrorLabel = QLabel("Absolute Relative Error", self)
        relativeErrorLabel.setObjectName('smallLabel')
        relativeErrorLabel.setWordWrap(True)
        relativeErrorLabel.setGeometry(510, 230, 160, 60)
        relativeErrorLabel.setVisible(False)

        relativeErrorInput = QLineEdit(self)
        relativeErrorInput.setGeometry(670, 230, 100, 50)
        relativeErrorInput.setVisible(False)

        LUFormComboBox = QComboBox(self)
        LUFormComboBox.addItem('Doolittle Form')
        LUFormComboBox.addItem('Crout Form')
        LUFormComboBox.addItem('Cholesky Form')
        LUFormComboBox.setGeometry(50, 350, 400, 75)  # Adjust the position
        LUFormComboBox.currentTextChanged.connect(lambda: LUForm(LUFormComboBox.currentText()))
        LUFormComboBox.setVisible(False)

        # Adding Number of Variables Label
        noOfVariablesLabel = QLabel("Number of Variables", self)
        noOfVariablesLabel.setObjectName('smallLabel')
        noOfVariablesLabel.setWordWrap(True)
        noOfVariablesLabel.setGeometry(510, 300, 160, 60)
        noOfVariablesLabel.setVisible(True)

        # Display Time Taken
        timeTaken = QLabel(self)
        timeTaken.setText(f"Time:          {self.time_taken}")
        timeTaken.setObjectName('smallLabel')
        timeTaken.setWordWrap(True)
        timeTaken.setGeometry(510, 400, 160, 60)
        timeTaken.setVisible(True)
        

        # Adding Number of Variables Input
        noOfVariablesInput = QLineEdit(self)
        noOfVariablesInput.setGeometry(670, 300, 100, 50)
        noOfVariablesInput.setVisible(True)
        noOfVariablesInput.returnPressed.connect(lambda : create_matrix(int(noOfVariablesInput.text())))  
        
        

        #Adding vertical line
        line = QFrame(self) 
        line.setGeometry(800, 0, 5, 900)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        # Adding Inital Guess Label
        self.initialGuessLabel.setObjectName('smallLabel')
        self.initialGuessLabel.setWordWrap(True)
        self.initialGuessLabel.setGeometry(850, 90, 160, 60)
        self.initialGuessLabel.setVisible(False)
    
        

        
        self.matrixInput.setGeometry(850, 300, 660, 590)
        self.matrixInput.setVisible(True)


        # Creating the Solution Label
        self.solutionLabel.setObjectName("smallLabel")
        self.solutionLabel.setGeometry(50, 620, 800, 200)
        self.solutionLabel.setVisible(False)

        #Creating the Solution Output
        self.solutionOutput.setGeometry(45, 750, 700, 70)
        self.solutionOutput.setVisible(False)
        
     
        
        def create_matrix( noOfVariables):

            # clear
            if self.matrixInput is not None:
                self.matrixInput.deleteLater()
            self.initialGuessLabel.setVisible(False)
    
            if self.initialGuessInput is not None:
                self.initialGuessInput.deleteLater()
            


            self.matrixInput = QScrollArea(self)
            self.matrixInput.setGeometry(850, 300, 660, 590)
            self.matrixInput.setVisible(True)

            self.initialGuessInput = QScrollArea(self)
            self.initialGuessInput.setGeometry(850, 160, 660, 100)
            self.initialGuessInput.setVisible(False)

            # Create the content widget for the matrix scroll area
            matrix_content_widget = QWidget()
            self.matrixInput.setWidget(matrix_content_widget)

            # Set the layout for the content widget as QVBoxLayout for vertical arrangement
            matrix_layout = QVBoxLayout(matrix_content_widget)

            initial_guess_content_widget = QWidget()
            self.initialGuessInput.setWidget(initial_guess_content_widget)

            initial_guess_layout = QHBoxLayout(initial_guess_content_widget)
            
            # Repeat the matrix lines vertically based on the noOfVariables
            for _ in range(noOfVariables):
                matrix_line_layout = QHBoxLayout()  # Create a new QHBoxLayout for eas line

                # write the number of the equation
                equationNumberLabel = QLabel(f"Eq {_ + 1}:", self)
                equationNumberLabel.setObjectName('smallLabel')
                equationNumberLabel.setFixedSize(50, 50)
                matrix_line_layout.addWidget(equationNumberLabel)

                for i in range(1, noOfVariables + 1):
                    matrix_edit_line = QLineEdit(self)
                    matrix_line_layout.addWidget(matrix_edit_line)

                    if i < noOfVariables:
                        plus_label = QLabel(f'x{i} +', self)
                        plus_label.setObjectName('smallLabel')
                        plus_label.setFixedSize(70, 50)
                        matrix_line_layout.addWidget(plus_label)

                equals_label = QLabel(f'x{i} =', self)
                equals_label.setObjectName('smallLabel')
                matrix_line_layout.addWidget(equals_label)

                result_edit_line = QLineEdit(self)
                matrix_line_layout.addWidget(result_edit_line)


                # Add the line layout to the matrix layout
                matrix_layout.addLayout(matrix_line_layout)
                print("matrix_layout.count() = ", matrix_layout.count())



            initial_guess_content_widget = QWidget()
            self.initialGuessInput.setWidget(initial_guess_content_widget)
            initial_guess_layout = QHBoxLayout(initial_guess_content_widget)  # Create a new QHBoxLayout for eas line

            for i in range(1, noOfVariables + 1):
                label = QLabel(f'x{i} =', self)
                label.setObjectName("smallLabel")
                initial_guess_layout.addWidget(label)

                edit_line = QLineEdit(self)
                initial_guess_layout.addWidget(edit_line)



            if combo_box.currentText() == 'Gauss-Seidel Iteration' or combo_box.currentText() == 'Jacobi Iteration':
                self.initialGuessLabel.setVisible(True)
                self.initialGuessInput.setVisible(True)
            
            self.matrixInput.setWidgetResizable(True)
            self.initialGuessInput.setWidgetResizable(True)

                
        def solve():
            
            self.solutionLabel.setText("ٍSolution")

            # clear
            self.solutionLabel.setVisible(True)
            self.solutionOutput.deleteLater()



            self.solutionOutput = QScrollArea(self)
            self.solutionOutput.setGeometry(50, 750, 700, 100)
            self.solutionOutput.setVisible(True)
            
            solution_content_widget= QWidget()
            self.solutionOutput.setWidget(solution_content_widget)

            # Set the layout for the content widget as QVBoxLayout for vertical arrangement
            output_layout = QHBoxLayout(solution_content_widget)

            # Create the content widget for the matrix scroll area
            rendered_text = ""

            

            self.solutionOutput.setWidgetResizable(True)

            output = None

            # Gathering Data
            num_variables = noOfVariablesInput.text()
            current_method = combo_box.currentText()
            sig_fig = sigFigInput.text()



            arr = [[] for _ in range(int(num_variables))]
            


            res = [1]

            print("arr" , arr)

            # Retrieve the content widget from the initialGuessInput scroll area
            content_widget = self.matrixInput.widget()
            print(type(content_widget))

            # Check if the content widget is a QWidget and has a layout
            if isinstance(content_widget, QWidget):
                print("res", res)
                line_layout = content_widget.layout()
                print("type of line_layout",type(line_layout))

                # Check if the layout exists
                if line_layout:
                    # Iterate through the layout and read into the array
                    for i in range(line_layout.count()):
                        
                        item = line_layout.itemAt(i)
                        if item.layout():
                            for j in range(item.layout().count()):
                                item2 = item.layout().itemAt(j)
                                if item2.widget() and isinstance(item2.widget(), QLineEdit):
                                    edit_line = item2.widget()
                                    print("i = ", i, "j = ", j)

                                    arr[i].append(float(edit_line.text()))
                                    print("appended ", float(edit_line.text()), "to arr[", i, "]")


            conv = ""
            print("arr = ", arr)
            coefficients = [row[:-1] for row in arr]
            constants = [row[-1] for row in arr]

            # Switching between methods
            if current_method == 'Gauss Elimination':
                gaussElimination = GaussElimination()
                gaussElimination.PRESCION = int(sig_fig)
                
                gaussElimination.calculate(arr)
                res = gaussElimination.res
                self.steps = gaussElimination.list_array
                self.time_taken = gaussElimination.time_taken
                timeTaken.setText(f"Time:          {self.time_taken}")
                conv = gaussElimination.status

            elif current_method == 'Gauss-Jordan Elimination':
                gaussJordan = GuassJordan()
                gaussJordan.calculate(arr)
                res = gaussJordan.res
                self.steps = gaussJordan.list_array
                self.time_taken = gaussJordan.time_taken
                timeTaken.setText(f"Time:          {self.time_taken}")

            elif current_method == 'LU Decomposition':
                current_decomposition = LUFormComboBox.currentText()
                print("coefficients, constants, current_decomposition, int(sig_fig)")
                print(coefficients, constants, current_decomposition, int(sig_fig))
                L, U, res, self.time_taken, error, self.steps = LuDecompositionSolver().solve(arr, current_decomposition, int(sig_fig))
                print(self.time_taken)
                timeTaken.setText(f"Time:          {self.time_taken}")
            elif current_method == 'Jacobi Iteration' or current_method == 'Gauss-Seidel Iteration':

                
                time_start=time.time()
                print("coefficients = ", coefficients)
                print("constants = ", constants)

                initial_guess = []

                content_widget = self.initialGuessInput.widget()
                print(type(content_widget))

                # Check if the content widget is a QWidget and has a layout
                if isinstance(content_widget, QWidget):
                    initial_guess_layout = content_widget.layout()
                    print(type(initial_guess_layout))

                    # Check if the layout exists
                    if initial_guess_layout:
                        # Iterate through the layout  and read into the initial_guess
                        for i in range(initial_guess_layout.count()):
                            item = initial_guess_layout.itemAt(i)
                            if item.widget() and isinstance(item.widget(), QLineEdit):
                                edit_line = item.widget()
                                initial_guess.append(float(edit_line.text()))
                    else:
                        print("Layout is not set for initialGuessInput.")
                else:
                    print("Content widget is not a QWidget for initialGuessInput.")

                if combo_box.currentText() == 'Jacobi Iteration':
                    self.steps, conv = jacobi(coefficients, constants, initial_guess, int(noOfIterationInput.text()), int(sigFigInput.text()), float(relativeErrorInput.text()))
                    time_end=time.time()
                    self.time_taken = time_end - time_start
                    timeTaken.setText(f"Time:          {self.time_taken}")
                else:
                    self.steps, conv = gauss_seidel(coefficients, constants, initial_guess, int(noOfIterationInput.text()), int(sigFigInput.text()), float(relativeErrorInput.text()))
                    time_end=time.time()
                    self.time_taken = time_end - time_start
                    timeTaken.setText(f"Time:          {self.time_taken}")
                res = self.steps[-1]
            print("oj")
            print(res)
            print("oj")

            if len(res) != 0:

                if conv:
                    self.solutionLabel.setText(conv)
                    conv = ""

                for i in range(1, int(noOfVariablesInput.text()) + 1):
                    rendered_text += f"x{i} = {res[i-1]}"
                    if i < int(noOfVariablesInput.text()):
                        rendered_text += ", "
            else:
                self.solutionLabel.setText("No Solution")

            
            
            output_label = QLabel(rendered_text, self)
            output_label.setObjectName("smallLabel")
            output_layout.addWidget(output_label)
            
            


        

    
            

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_()) 