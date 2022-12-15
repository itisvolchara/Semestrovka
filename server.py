from socket import socket
import threading
from random import choice


def handle_word(input_word, correct_word):
    if len(input_word) != 5:
        return False

    input_word = input_word.upper()
    correct_word = correct_word.upper()

    if any(map(lambda letter: ord(letter) < 65 or ord(letter) > 90, input_word)):
        return False

    check_dict = [[letter, 0] for letter in input_word]
    for i in range(5):
        if check_dict[i][0] in correct_word:
            check_dict[i][1] = 1
            if input_word[i] == correct_word[i]:
                check_dict[i][1] = 2

    return check_dict

def client_handle(client_listen, client_send):
    while True:
        pass

def library_generate():
    return choice(['hello', 'start', 'world', 'begin', 'digit', 'joker', 'width', 'alpha', 'gamer'])


def main():
    server = socket()
    server.bind(('127.0.0.1', 1234))
    server.listen()
    server_on = True

    clients = []
    for i in range(2):
        client, adress = server.accept()
        clients.append(client)

    threading.Thread(target=client_handle, args=(clients[0], clients[1],)).start()
    threading.Thread(target=client_handle, args=(clients[1], clients[0],)).start()

    game_on = True

    while server_on:
        correct_word = word_generate()
        print(f"the word is {correct_word}")
        attempts = 0

        while game_on:
            message = client.recv(1024).decode("utf8")
            print(f"Got the message \n{message}")

            checking = handle_word(message, correct_word)

            answer = ''
            stat_total = 0
            if not checking:
                answer += f"<> --error-- {attempts}"
            else:
                attempts += 1
                answer = '<'
                for i in range(5):
                    answer += f"{checking[i][0]}_{checking[i][1]}_"
                    stat_total += checking[i][1]

                answer = answer[0:-1] + "> "

                if stat_total == 10:
                    answer += "--win-- "
                    game_on = False
                elif attempts == 6:
                    answer += "--lose-- "
                    game_on = False
                else:
                    answer += "--continue-- "
                answer += str(attempts)

            print(f"Sending message \n{answer}")
            client.send(answer.encode("utf8"))

        message = client.recv(1024).decode("utf8")
        if message == "--restart--":
            answer = f"<> --restart-- {attempts}"
            game_on = True
        else:
            answer = f"<> --game_over-- {attempts}"
            server_on = False
        client.send(answer.encode("utf8"))

    server.close()


if __name__ == "__main__":
    main()