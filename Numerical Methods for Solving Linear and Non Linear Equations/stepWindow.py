from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtWidgets import *

class StepWindow(QMainWindow):

    def __init__(self, answer=[],
                  method='',sig_fig=5):

        super().__init__()

        self.setObjectName("StepWindow")

        # Set the size of the main window
        self.setGeometry(100, 100, 800, 600)  # Set width and height
        

        # Set the window title
        self.setWindowTitle("Equations Calculator")

        self.step = 0

        self.answer = answer

        self.method = method

        self.sig_fig = sig_fig

        # Set the window icon
        self.setWindowIcon(QIcon("gui\icons\sigma_icon.png"))
        self.initUI()

        with open("gui/themes/design1.qss") as f:
            self.setStyleSheet(f.read())

    def nextStepGauss(self, answer):
        # Stop if the steps are printed
        if self.step >= len(answer) or 0 == len(answer[self.step]):
            return

        noOfCols = len(answer[self.step][0])

        noOfRows = len(answer[self.step])

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(100*noOfCols, 100*noOfRows)
        new_frame.setFrameShape(QFrame.NoFrame)

        widget = QWidget(self.centralwidget)
        widget.setGeometry(QtCore.QRect(10, 10, 201, 121))
        widget.setObjectName("widget_2")
        
        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # Trying sth for better UI/UX
        label = QLabel(widget)
        label.setObjectName(u"smallLabel")

        label.setText(_translate("MainWindow", f"Step {self.step + 1}: "))

        gridLayout.addWidget(label, 0, 0, 1, 1)

        # Solution matrix creation
        for i in range(noOfRows):

            for j in range(noOfCols):

                label = QLabel(widget)
                label.setObjectName('smallLabel')
                label.setText(_translate("MainWindow", f"{answer[self.step][i][j]}"))
                gridLayout.addWidget(label, i, j+1, 1, 1)

        layout = QHBoxLayout(new_frame)
        layout.addWidget(widget)

        frame_layout.addWidget(new_frame)

        self.step += 1
    
    def nextStepLU(self, answer):

        # Stop if the steps are printed
        if self.step >= len(answer):
            return

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(100*self.sig_fig, 90)
        new_frame.setFrameShape(QFrame.NoFrame)

        widget = QWidget(self.centralwidget)
        widget.setGeometry(QtCore.QRect(10, 10, 100, 100))
        widget.setObjectName("widget_2")
        
        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # Displaying the current step
        label = QLabel(widget)
        label.setObjectName(u"smallLabel")

        label.setText(_translate("MainWindow", f"Step {self.step + 1}: {answer[ self.step ]}"))

        gridLayout.addWidget(label)

        layout = QHBoxLayout(new_frame)
        layout.addWidget(widget)

        frame_layout.addWidget(new_frame)

        self.step += 1

    def nextStepIterative(self, answer):
    
        # Stop if the steps are printed
        if self.step >= len(answer) or 0 == len(answer[self.step]):
            return
        
        size = len(answer[self.step])


        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(100*self.sig_fig, 80*size)
        new_frame.setFrameShape(QFrame.NoFrame)

        widget = QWidget(self.centralwidget)
        widget.setGeometry(QtCore.QRect(10, 10, 100, 100))
        widget.setObjectName("widget_2")
        
        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        label = QLabel(widget)
        label.setObjectName(u"smallLabel")

        label.setText(_translate("MainWindow", f"Step {self.step + 1}: "))

        gridLayout.addWidget(label, 0, 0, 1, 1)

        i = self.step

        # iteration creation

        for i in range(len(answer[ self.step ])):

            label = QLabel(widget)
            label.setObjectName('smallLabel')
            label.setText(_translate("MainWindow", f"x{i+1}={answer[ self.step ][i]}"))
            gridLayout.addWidget(label, i, 1, 1, 1)



        layout = QHBoxLayout(new_frame)
        layout.addWidget(widget)

        frame_layout.addWidget(new_frame)

        self.step += 1
    
    def bracketing(self, answer):
        # Stop if the steps are printed
        if self.step >= len(answer):
            return

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(600, 150)
        new_frame.setFrameShape(QFrame.NoFrame)

        gridLayout = QGridLayout(new_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # iteration creation
        x_up, x_lw, f_x_up, f_x_lw, error = answer[ self.step ].getStep()
        label = QLabel(new_frame)
        label.setObjectName('smallLabel')
        label.setText(_translate("MainWindow", f"Step {self.step + 1}:\txl={x_lw}\n\t xu={x_up}\n\t f(xl)={f_x_lw}\n\t f(xu)={f_x_up}\n\t ea={error}"))
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignLeft)
        gridLayout.addWidget(label)
        
        frame_layout.addWidget(new_frame)

        self.step += 1

    def fixed(self, answer):
        # Stop if the steps are printed
        if self.step >= len(answer):
            return

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(600, 150)
        new_frame.setFrameShape(QFrame.NoFrame)

        gridLayout = QGridLayout(new_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # iteration creation
        x0, x1, error = answer[ self.step ]
        label = QLabel(new_frame)
        label.setObjectName('smallLabel')
        label.setText(_translate("MainWindow", f"Step {self.step + 1}:\txi= {x0}\n\t xi+1= {x1}\n\t ea= {error}"))
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignLeft)
        gridLayout.addWidget(label)
        
        frame_layout.addWidget(new_frame)

        self.step += 1

    def secant(self, answer):
        # Stop if the steps are printed
        if self.step >= len(answer):
            return

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(600, 150)
        new_frame.setFrameShape(QFrame.NoFrame)

        gridLayout = QGridLayout(new_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # iteration creation
        iter_count, x_prev, x_curr, x_next, ea = answer[ self.step ]
        label = QLabel(new_frame)
        label.setObjectName('smallLabel')
        label.setText(_translate("MainWindow", f"Step {self.step + 1}:\txi-1={x_prev}\n\t xi={x_curr}\n\t xi+1={x_next}\n\t ea={ea}"))
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignLeft)
        gridLayout.addWidget(label)
        
        frame_layout.addWidget(new_frame)

        self.step += 1

    def newton_0_1(self, answer):
        # Stop if the steps are printed
        if self.step >= len(answer):
            return

        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame.setFixedSize(600, 150)
        new_frame.setFrameShape(QFrame.NoFrame)

        gridLayout = QGridLayout(new_frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")

        _translate = QtCore.QCoreApplication.translate

        # iteration creation
        x0, x1, f_x, f_d, error = answer[ self.step ].getStep()
        label = QLabel(new_frame)
        label.setObjectName('smallLabel')
        label.setText(_translate("MainWindow", f"Step {self.step + 1}:\txi={x0}\n\t xi+1={x1}\n\t f(x)={f_x}\n\t f'(x)={f_d}\n\t ea={error}"))
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignLeft)
        gridLayout.addWidget(label)
        
        frame_layout.addWidget(new_frame)

        self.step += 1


    def initUI(self):

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        main_window = QWidget()
        main_window.setGeometry(100, 100, 300, 300)

        # Create Scroll area for Step Mode
        scroll_area = QScrollArea(self.centralwidget)
        scroll_area.setGeometry(0, 0, 800, 600)
        scroll_area.setStyleSheet(
            "border: none; padding: 0px;"
        )

        # Create main frame for Step Mode
        global frame_layout
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)

        scroll_widget = QWidget()
        scroll_widget.setLayout(frame_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # Create Next step Button for Step Mode
        button = QPushButton('Next Step', self.centralwidget)
        button.setObjectName(u"smallLabel")
        button.setGeometry(550, 255, 180, 80)
        print(self.method)
        # Choose the method depend on app.py
        if self.method == "Gauss Elimination" or self.method == 'Gauss-Jordan Elimination':
            self.step = 0
            button.clicked.connect(lambda: self.nextStepGauss(self.answer))
        elif self.method == 'LU Decomposition':
            self.step = 0
            button.clicked.connect(lambda: self.nextStepLU(self.answer))
        elif self.method == 'Gauss-Seidel Iteration' or self.method == 'Jacobi Iteration':
            self.step = 0
            button.clicked.connect(lambda: self.nextStepIterative(self.answer))
        elif self.method == "Bisection" or self.method == "False-Position":
            self.step = 0
            button.clicked.connect(lambda: self.bracketing(self.answer))
        elif self.method == "Fixed point":
            self.step = 0
            button.clicked.connect(lambda: self.fixed(self.answer))
        elif self.method == "Secant":
            self.step = 0
            button.clicked.connect(lambda: self.secant(self.answer))
        elif self.method == "Original Newton-Raphson" or self.method == "Modified Newton-Raphson 2" or self.method == "Modified Newton-Raphson 1":
            self.step = 0
            button.clicked.connect(lambda: self.newton_0_1(self.answer))

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    

        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = StepWindow(answer=[
            "Swap 1",
            "x[\theta]=0.5",
            "x[ 1 ] = 4.9",
            "x[2]=3.0924444444444444444444444444444444444444444444444444444444444444444444444444444444443",
            "Swap 2",
            "x[\theta]=0.14679",
            "x[1]=3.7153",
            "x[ 2]",
            "3.8118",
            "Swap 3",
            "x[0] = 0.74275",
            "x[1] 3.1644",
            "x[ 2]                       3.9708",
            "Swap 4",
            "x[\theta]=0.94675",
            "x[1] 3.0281",
            "x[2]=3.9971",
            "Swap 5",
            "x[0]=0.99177",
            "x[1] 3.0034",
            "x[ 2 ] = 4.0001",
            "Swap 6",
            "x[0] = 0.99919",
            "x[1] 3.0001",
            "x[ 2] 4.0001"
            ], method='LU Decomposition')
    ui.show()
    sys.exit(app.exec_())
