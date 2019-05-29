# Python program to implement server side of chat room. 
import socket, select, sys, _thread

commands = {'help': 'Commands are /help, /take, /ping',
            'Age': 7,
}

  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 2: 
    print("Correct usage: script, IP address, port number")
    exit() 
  
# takes the first argument from command prompt as IP address 
HOST = socket.gethostname()

  
# takes second argument from command prompt as port number 
PORT = int(sys.argv[1]) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((HOST, PORT)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
print("Listening on", HOST, PORT)
server.listen(100) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    conn.send(bytes('Welcome to ' + HOST + '\'s chatroom!', 'utf8'))
    # conn.send(bytes('Welcome to ' + HOST + '\'s chatroom!\n', 'utf8'))

  
    while True: 
            try: 
                message = conn.recv(1024).decode('utf-8')
                if message: 
                    # remove trailing whitespace and newlines
                    message.rstrip()

                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    print("<" + addr[0] + "> " + message)

                    """do not broadcast if user message prepended 
                    with a '/' indicating a command"""
                    if (message[:1] == '/'):
                        inputCommand(conn, message[1:])
                        
                    else:
                        # Calls broadcast function to send message to all 
                        message_to_send = "<" + addr[0] + "> " + message
                        broadcast(message_to_send, conn) 
  
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn) 
  
            except: 
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for client in list_of_clients: 
        if client!=connection: 
            try: 
                client.send(bytes(message, 'utf8'))
            except: 
                client.close() 
                # if the link is broken, we remove the client 
                remove(client) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        # print("Removing client: " + connection)
        list_of_clients.remove(connection) 

def inputCommand(conn, message):
    # conn.send(bytes(("YOU SAID " + message), 'utf8'))
    if message in commands:
        print("SHOULD SEND " + commands[message])
        conn.send(bytes(commands[message]), 'utf8') 
    else:
        conn.send(bytes("Command not recognized"), 'utf8')
  
while 1: 
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 
  
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 
  
    # prints the address of the user that just connected 
    # print(addr[0] + " connected")
    connMessage = addr[0] + " connected"
    
    for address in list_of_clients:
        broadcast(connMessage, address)
    
    # creates and individual thread for every user  
    # that connects 
    _thread.start_new_thread(clientthread, (conn,addr))  
    # clientthread(conn, addr)   
  
conn.close()
server.close()