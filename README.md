# TCP Chat Program
This project contains a TCP client and server. They interact with one another by sending command and data messages. Commands always start with "C " and data containing messages always start with "D ".

## Running the Server Application
To run the server, enter:

```python3 server-v3.py <hostname> <port_number> ```

## Running the Client Application
To run the server, enter:

```python3 server-v3.py <server's hostname> <server's port_number> <username>```

### Demonstration

![TCP chat program demonstration. Three client terminals and one server terminal](./three%20clients%20and%20one%20server.png)

## Understanding how the applications work
The server application will always have a thread running which will listen for clients. Once a client is received, it will append the client's name and socket into respective list arrays. The server listening thread will create a separate thread to receive this client.

The client contains two active threads. One thread receives messages from the server and the other takes in input from the user and sends it to the server. This information can be either a command or message data. 

Command data is denoted by a "C " at the start of the input. There are three commands.

## The Direct Message command (C DM)
This command is initiated by typing in ```C DM```. This will then list the names of all active users and the client will be prompted to type in the name of a message recipient, in the format ```C <client_name>```. Afterwards, the user will be prompted to enter a message, which must me done in the form ```D <message>```. 

Incorrect user input will result in a claryfying message and will return the user to command mode. 

## The Public Message command (C PM)
This command is initiated by typing in ```C PM```. This prompts the user for a public message, which is entered in the form ```D <message>```.

Incorrect user input will result in a claryfying message and will return the user to command mode. 

## The Exit command (C EX)
This command is entered by typing in ```C EX```. It will cause the sending thread of the client to send a exit command to the client, before it breaks and ends. The receiving thread is killed when it receives a kill command from the user. It waits for the sending thread to end with ```threading.Thread.join(receive_thread)``` and exits as well. 

The exit command will remove the client's name and socket from the server's name and socket arrays. This ensures that other clients are aware that the user has disconnected.

## Issues in implementation
For the most part, the client and server work as intended. When multiple terminals are used on one computer, the terminals sometimes crash because of KeyboardInterrupt errors.

I've included previous versions of my project to demonstrate my progress.