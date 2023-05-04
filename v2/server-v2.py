# This is the client function
import threading
import socket
import sys

# TODO for server
# implement commands and data. Commands start with 'C' and data with 'D'
# commands include 'EX' to exit, 'PM' for a private message, and 'DM' for a direct message

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
            client.send("You are in command mode".encode('utf-8'))
            message = client.recv(1024).decode()
            match message:
                case 'C EX':
                    client.send("C EX".encode('utf-8'))
                    # Remove from name and socket arrays
                    index = client_sockets.index(client)
                    client_sockets.remove(client)
                    name = client_names[index]
                    client_names.remove(name)
                    print(f'Client {name} has been removed')
                    break;
                case 'C PM':
                    client.send("Please enter a public message:".encode('utf-8'))
                    message = client.recv(1024).decode();
                    if message.startswith('D '):
                        message.lstrip('D ')
                    send_pm(message.encode('utf-8'))
                case 'C DM':
                    # Sending the list of client names as a string
                    message = "The available clients are: "
                    for name in client_names:
                        message = message + name + " "
                    client.send(message.encode('utf-8'))

                    message = client.recv(1024).decode()
                    index = client_names.index(message)
                    reciever = client_sockets[index]

                    client.send(f"Type a message for {message}:".encode('utf-8'))
                    message = client.recv(1024).decode()
                    if message.startswith('D '):
                        message.lstrip('D ')
                    send_dm(message.encode('utf-8'), reciever)

        except:
            # If the client is not responsive, remove it from the active list and end its thread
            # index is used to find matching name in name array
            index = client_sockets.index(client)
            client_sockets.remove(client)
            name = client_names[index]
            client_names.remove(name)
            # THIS RESULTS IN THE THREAD ENDING.
            break

# This function receives connections
# If a connection is detected, it will create a new thread for it
# IMPLEMENT COMMAND MODE AND DATA MODE
def receive_clients():
    while True:
        print('The server is running and listening')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')

        # This message won't be printed by the client. Just used to prompt the name
        client.send("C name".encode('utf-8'))
        name = client.recv(2014).decode()
        client_sockets.append(client) # save socket in socket array
        client_names.append(name) # save name in name array

        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()
        
# If these two threads are the same, then we are in the main thread
# While the main thread is active, it will receive clients and give them a thread
# Main thread dies = entire server dies. Client thread dies = that client disconnects
if threading.current_thread() is threading.main_thread():
    receive_clients()