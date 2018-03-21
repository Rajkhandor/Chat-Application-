#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)
#print(ADDR)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():

    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please enter your name", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


def handle_client(client):  # Takes client socket as argument.

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! You are connected to the chat .' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("\quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("\quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


