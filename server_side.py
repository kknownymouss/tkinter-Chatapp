import socket
import threading
from colorama import Fore, init

# INITIALIZING COLORAMA
init()


# DECLARING CONSTANTS
PORT = 5050 # Here goes the port you want the people to connect to
SERVER = "0.0.0.0" # Here goes the ip address you want the server to run on
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
BUFSIZ = 512

# DECLARING VARIABLES
clients = []
messages = []

# INITIALIZING SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def broadcast_username(username):
    for client in clients:
        client.send(f"  {username} has connected.".encode(FORMAT))


def broadcast_message(username, message):
    for client in clients:
        client.send(f"  [{username}]  {message}".encode(FORMAT))


def broadcast_exit_message(username):
    for client in clients:
        client.send(f"  {username} has left the chat.".encode(FORMAT))


def start():
    try:
        print(f"[STARTING] Server is starting..." + "\n")
        server.listen()
        print(Fore.GREEN + f"[LISTENING] Server is listening on {SERVER}", Fore.RESET, "\n")
        while True:
            conn, addr = server.accept()
            clients.append(conn)
            thread1 = threading.Thread(target=handle_clients, args=(conn, addr))
            thread1.start()
    except Exception as e:
        print(Fore.RED + "[ERROR] Please try again", Fore.RESET)


def handle_clients(connection, address):
    client_username = connection.recv(BUFSIZ).decode(FORMAT)
    broadcast_username(client_username)
    print(Fore.GREEN + f"{client_username} has connected !", Fore.RESET)
    while True:
        try:
            client_message = connection.recv(BUFSIZ).decode(FORMAT)
            if client_message == "!1!2!3!":
                broadcast_exit_message(client_username)
                print(Fore.RED + f"{client_username} has left the chat." + Fore.RESET)
                connection.close()
                clients.remove(connection)
                break
            else:
                broadcast_message(client_username, client_message)
                print(f"[{client_username}] {client_message}")
        except:
            print(Fore.RED + f"{client_username} has left the chat." + Fore.RESET)
            connection.close()
            clients.remove(connection)
            break



start()
