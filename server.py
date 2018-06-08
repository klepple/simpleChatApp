# This is the server that handles the chat clients
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


def accept_connections():  # target of main application thread
    """Handling incoming client connections"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("You have successfully connected to the chat server! Please enter your name: ", "utf8"))
        addresses[client] = client_address  # store client's address in the address list
        # create a thread to handle the client
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # target of client thread
    """Handling a single client"""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Welcome %s to the best chat server EVER!! If you want to quit at any point, please type !quit." % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat room! REJOICE " % name
    broadcast(bytes(msg, "utf8"))  # tell everyone about the new user
    clients[client] = name
    while True:  # handle incoming messages
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat room. Sad." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


# constants
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
# create server socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)  # listens for 5 connections
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()  # start infinite loop
    ACCEPT_THREAD.join()  # join so that main script waits for the thread to complete before closing the server
    SERVER.close()
