import threading
import socket

host = "127.0.0.1"
port = 1234

server = socket.socket()
server.bind((host, port))
server.listen()


def handle(number):
    while True:
        message = clients[number].recv(1024).decode('utf8')
        clients[number-1].send(message.encode('utf8'))


def receive():

    for i in range(2):
        client, address = server.accept()
        clients.append(client)
        print("Connected with {}".format(str(address)))

        thread = threading.Thread(target=handle, args=(i,))
        thread.start()


if __name__ == '__main__':
    clients = []
    receive()
