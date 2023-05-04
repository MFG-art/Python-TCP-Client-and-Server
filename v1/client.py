import threading
import socket
import sys

# Client must be run like "python client.py host port username"
name = sys.argv[3]
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], int(sys.argv[2]))) # (host, port)

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "Name?":
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

def client_send():
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target = client_receive)
receive_thread.start()
if threading.current_thread() is threading.main_thread():
    client_send()