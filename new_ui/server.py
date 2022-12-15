from socket import socket
import threading

client_counter = 0


def handle(client):
    global client_counter

    while True:
        message = client.recv(1024).decode('utf8')

        number, request_status, word = message.split()
        response = number
        if request_status == '--start--':
            if client_counter == 1:
                response = "1 --start_word-- <>"
            elif client_counter == 2:
                response = "2 --start_guess-- <>"
        client.send(response.encode('utf8'))

def main():
    host = "127.0.0.1"
    port = 1234

    server = socket()
    server.bind((host, port))
    server.listen()

    global client_counter

    for i in range(2):
        client, _ = server.accept()
        client_counter += 1
        threading.Thread(target=handle, args=(client,)).start()


if __name__ == "__main__":
    main()