import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
