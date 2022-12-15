import sys
from time import sleep

from socket import socket

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window_new import Ui_StartWindow


class StartWindow(QMainWindow, Ui_StartWindow):
    def __init__(self):
        self.client = None

        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)

    def start(self):
        self.label_2.setText("Loading")
        self.label_2.show()
        self.client = socket()
        while True:
            try:
                self.client.connect(("127.0.0.1", 1234))
                break
            except ConnectionRefusedError:
                sleep(1)
        self.client.send("0 --start-- <>")

        self.handle()

    def handle(self):
        message = self.client.recv(1024).decode('utf8')

        number, response_status, word = message.split()
        if response_status == "--start_word--":
            self.label_2.setText("Start word")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = StartWindow()

    window.show()
    sys.exit(app.exec())