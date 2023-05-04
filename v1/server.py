# This is the client function
import threading
import socket
import sys

host = sys.argv[1]
port = sys.argv[2]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(port)))
server.listen()

# These are used to handle and store client
# Each client has their own index (client_sockets[i], client_names[i])
client_sockets = []
client_names = []

def send_pm(message):
    for client in client_sockets:
        client.send(message)

def send_dm(message, client):
    client.send(message)

# handle_client is called as a separate thread
# here, the server receives commands from the client, as well as messages
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            send_pm(message)
        except:
            # If the client is not responsive, remove it from the active list and end its thread
            # index is used to find matching name in name array
            index = client_sockets.index(client)
            client_sockets.remove(client)
            client_names.remove(client)
            name = client_names[client]
            client_names.remove(name)
            # THIS RESULTS IN THE THREAD ENDING.
            break

# This function receives connections
# If a connection is detected, it will create a new thread for it
def receive_clients():
    while True:
        print('The server is running and listening')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send("Name?".encode('utf-8'))
        name = client.recv(2014).decode()
        client_sockets.append(client)
        client_names.append(name)
        print(f"The name of the new client is {name}")
        send_pm(f"{name} has connected to the chatroom".encode('utf-8'))
        client.send("You are now connected".encode('utf-8'))
        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()
        
# If these two threads are the same, then we are in the main thread
if threading.current_thread() is threading.main_thread():
    receive_clients()