import threading
import socket
import sys # for sys.argv

# TODO for client
# implement commands and data. Commands start with 'C' and data with 'D'
# commands include 'EX' to exit, 'PM' for a private message, and 'DM' for a direct message

# Client must be run like "python client.py host port username"
name = sys.argv[3]
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], int(sys.argv[2]))) # (host, port)

# This function takes care of receiving messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "C name":
                client.send(name.encode('utf-8'))
            elif message == "C EX":
                break;
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

# This function sends to the server
def send():
    while True:
        message = f'{input("")}'
        client.send(message.encode('utf-8'))
        if message == "C EX":
            threading.Thread.join(receive_thread)
            break;

# Create and start separate thread for receive()
receive_thread = threading.Thread(target = receive)
receive_thread.start()

# The send() function will run in the main thread
if threading.current_thread() is threading.main_thread():
    send()