import threading
import socket

client = socket.socket()


def get_message():
    while True:
        message = client.recv(1024).decode('utf8')
        print(message)


def send_message():
    while True:
        message = input()
        client.send(message.encode('utf8'))


def handle():
    client.connect(("127.0.0.1", 1234))

    thr = threading.Thread(target=get_message)
    thr.start()
    thr = threading.Thread(target=send_message)
    thr.start()


if __name__ == "__main__":
    handle()
