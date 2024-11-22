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
from app import MyWindow
from app2 import MyWindow2

class OptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("OptionWindow")

        # Set the size of the main window
        self.setGeometry(200, 200, 600, 300)  # Set width and height
        

        # Set the window title
        self.setWindowTitle("Equations Calculator")

        # Set the window icon
        self.setWindowIcon(QIcon("gui\icons\sigma_icon.png"))
        self.initUI()

        with open("gui/themes/design1.qss") as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        self.setWindowTitle('Option Window')

        # Create buttons
        btn_linear = QPushButton('Linear System of Equations', self)
        btn_non_linear = QPushButton('Non-Linear System of Equations', self)
        btn_linear.setObjectName(u"smallLabel")
        btn_non_linear.setObjectName(u"smallLabel")
        btn_non_linear.setGeometry(QtCore.QRect(100, 70, 400, 70))
        btn_linear.setGeometry(QtCore.QRect(100, 150, 400, 70))

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(btn_linear)
        layout.addWidget(btn_non_linear)

        self.setLayout(layout)

        # Connect button click events to functions
        btn_linear.clicked.connect(self.show_linear_window)
        btn_non_linear.clicked.connect(self.show_non_linear_window)

    def show_linear_window(self):
        self.ui1 = MyWindow()
        self.ui1.show()
        self.close()

    def show_non_linear_window(self):
        self.ui2 = MyWindow2()
        self.ui2.show()
        self.close()







if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = OptionWindow()
    main_window.show()
    sys.exit(app.exec_())