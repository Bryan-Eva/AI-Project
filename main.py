import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout
from mainApp import MainApp


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if "__main__" == __name__:
    # TODO: PyQt- homepage
    # TODO: PyQt- coursepage
    main()
