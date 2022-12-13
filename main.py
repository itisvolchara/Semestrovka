import sys
from typing import List
from time import sleep

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window import Ui_MainWindow

from socket import socket


class Cell:
    def __init__(self, label):
        self.text = ''
        self.status = 0
        self.label = label

    def show(self):
        self.label.setText(self.text)
        if self.status == 1:
            self.label.setStyleSheet("background-color: white; border: 2px solid yellow; color: black")
        elif self.status == 2:
            self.label.setStyleSheet("background-color: yellow; border: 2px solid yellow")
        elif self.status == 0:
            self.label.setStyleSheet("background-color: gray; border: 2px solid yellow; color: white")
        else:
            self.label.setStyleSheet("background-color: black; border: 2px solid yellow")
        self.label.show()


class Line:
    def __init__(self, cells: List):
        self.cells = [Cell(label) for label in cells]
        self.status = []
        self.word = ''

    def set_word(self, word: str, status: List[int]):
        self.status = status
        self.word = word
        for idx, c in enumerate(word):
            self.cells[idx].text = c.upper()
            self.cells[idx].status = status[idx]

    def clear(self):
        self.word = ''
        self.status = [0 for _ in range(5)]
        for i in range(5):
            self.cells[i].text = ''
            self.cells[i].status = 3

    def show(self):
        for cell in self.cells:
            cell.show()


class Matrix:
    def __init__(self, wnd: Ui_MainWindow):
        self.lines: List[Line] = []

        for row in range(6):
            labels = []
            for col in range(5):
                labels.append(getattr(wnd, f'label_{row + 1}_{col + 1}'))
            self.lines.append(Line(labels))

    def clear(self):
        for i in range(6):
            self.lines[i].clear()
            self.lines[i].show()

    def move_table(self, new_word_analysis, height):
        print(f"Starting to move table")
        for i in range(height - 1, 0, -1):
            self.lines[i].set_word(self.lines[i - 1].word, self.lines[i - 1].status)
            self.lines[i].show()

        new_word = ''
        new_status = []
        for i in range(5):
            new_word += new_word_analysis[i][0]
            new_status.append(new_word_analysis[i][1])

        self.lines[0].set_word(new_word, new_status)
        self.lines[0].show()
        print("Completed")


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.matrix = Matrix(self)
        self.client = client
        self.confirmButton.clicked.connect(self.send_get)

    def send_get(self):
        print("pressed")
        if self.confirmButton.text() == "Restart?":
            to_send = "--restart--"
        else:
            to_send = self.lineEdit.text()
            if to_send == '':
                to_send = ' '

        self.client.send(to_send.encode('utf8'))
        response = self.client.recv(1024).decode('utf8')

        decoding, status, attempts = response.split()

        if status == "--error--":
            self.set_info("Incorrect input", 'color: red; font-weight: 600')
            return
        elif status == "--restart--":
            self.set_info()
            self.matrix.clear()
            self.confirmButton.setText("OK")
            self.lineEdit.setEnabled(True)
            self.lineEdit.clear()
            self.confirmButton.setStyleSheet("border: 2px solid yellow; color: white; font-size: 20px")
        else:
            self.set_info()
            self.lineEdit.clear()
            check_dict = []
            for i in range(1, 18, 4):
                check_dict.append([decoding[i], int(decoding[i + 2])])

            self.matrix.move_table(check_dict, int(attempts))

            if status == "--win--" or status == "--lose--":
                self.restart_mode()
                if status == "--win--":
                    self.set_info("You won!", "color: green; font-weight: 600")
                else:
                    self.set_info("Game over.", "color: red; font-weight: 600")

    def set_info(self, message='', style_sheet=''):
        self.infotable.setText(message)
        self.infotable.setStyleSheet(style_sheet)

    def restart_mode(self):
        self.lineEdit.setDisabled(True)
        self.confirmButton.setText("Restart?")
        self.confirmButton.setStyleSheet("border: 2px solid yellow; color: white; font-size: 14px")


def application():
    app = QApplication(sys.argv)

    client = get_connect()

    window = Window(client)

    window.show()
    sys.exit(app.exec())


def get_connect():
    client = socket()
    while True:
        try:
            client.connect(('127.0.0.1', 1234))
            return client
        except ConnectionRefusedError:
            sleep(1)


if __name__ == "__main__":
    application()
