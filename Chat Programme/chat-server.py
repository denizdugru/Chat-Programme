#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Weloome to chat room! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.

    name = client.recv(BUFSIZ).decode("utf8")
    print(name)
    welcome = 'Welcome %s! If you ever want to quit, type /quit to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        command_str = {}
        target_str = {}
        message_str = {}
        unsplitted_str = msg.decode("utf8") #TO CONTROL IF A MESSAGE CONTAINS COMMAND WE SPLIT STRINGS
        splitted_str = unsplitted_str.split()
        x = 0
        for p in splitted_str: #WE CAN EASILY DIVIDE COMMAND, TARGET CLIENT, AND MESSAGE BY THREE SEPERATE LISTS
            if x < 1:
                command_str[x] = p

            elif x == 1:
                target_str[x] = p

            elif x > 1:
                message_str[x] = p

            x = x + 1

        msg_new = ""
        for v in message_str:  #TO ADD ALL MESSAGE PARTS INTO ONE STRING
            msg_new = msg_new + message_str[v] + " "

        if command_str[0] == "/quit":
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

        elif command_str[0] == "/msg":
            target = target_str[1]
            target_conn = ""
            for x in clients:
                if clients[x] == target:
                    target_conn = x
                    break
                else:
                    print("Unable to reach %s" % target)
                    break
            target_conn.send(bytes(name, "utf8") + bytes(": ", "utf8") + bytes(msg_new, "utf8"))

        elif command_str[0] == "/help":
            help_ = "To quit type /quit and hit enter"
            help_2 = "To send a private message {/msg username your_message}"
            help_3 = "you need to type in this form without curly bracets"
            client.send(bytes(help_, "utf8"))
            client.send(bytes(help_2, "utf8"))
            client.send(bytes(help_3, "utf8"))

        else:
            broadcast(msg, name + ": ")


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 5001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(50)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
