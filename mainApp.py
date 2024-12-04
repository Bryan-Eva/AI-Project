import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout
from homepage import Ui_Form as HomePage
from chatPage import Ui_Form as ChatPage


class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("llama GPT")
        self.setObjectName("Main")
        self.resize(1000, 700)
        self.setStyleSheet(
            "#Main { border-image: url(./Qt/icons/Itsuki_4.jpg); }")

        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet(
            "QStackedWidget { background-color: rgba(0, 0, 0, 0.7); }")
        self.setCentralWidget(self.stacked)

        self.init_home_page()
        self.init_chat_page()

        self.stacked.setCurrentIndex(0)

    def init_home_page(self):
        home_page = HomePage()
        container = QWidget()
        home_page.setupUi(container)
        home_page.courseButton.clicked.connect(
            lambda _: self.stacked.setCurrentIndex(1))

        self.stacked.addWidget(container)

    def init_chat_page(self):
        chat_page = ChatPage()
        container = QWidget()
        chat_page.setupUi(container)

        self.stacked.addWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
