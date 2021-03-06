# Python program to implement server side of chat room. 
import socket, select, sys, _thread, time

commands = {'help': 'Commands: /help, /start, /take, /clear',
            'ping': 'pong!',
            'take': 'Attempted a take', 
            'start': 'Started',
            'yeet': 'YEET'
}

start = time.time()
running = False
  
'''
The first argument AF_INET is the address domain of the socket. 
This is used when we have an Internet Domain with any two hosts 
The second argument is the type of socket. SOCK_STREAM means 
that data or characters are read in a continuous flow.
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 2: 
    print("Correct usage: script, IP address, port number")
    exit() 
  
# takes the first argument from command prompt as IP address 
HOST = 'localhost' # socket.getfqdn()
  
# takes second argument from command prompt as port number 
PORT = int(sys.argv[1]) 
  
'''
Binds the server to an entered IP address and at the specified 
port number. The client must be aware of these parameters 
'''
server.bind((HOST, PORT)) 
  
'''
Listens for 100 active connections. This number can be increased 
as per convenience. 
'''
print("Listening on", HOST, PORT)
server.listen(1) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    conn.send(bytes('Welcome to ' + HOST + '\'s chatroom!\n', 'utf8'))
    conn.send(bytes('Try using \'/help\' to get started\n', 'utf8'))
  
    while True:

        try: 
            message = conn.recv(1024).decode('utf-8')
            if message: 
                # remove trailing whitespace and newlines
                message.rstrip()

                '''
                prints the message and address of the user who just 
                sent the message on the server terminal
                '''
                print("<" + addr[0] + "> " + message)


                # do not broadcast if user indicates a '/' (use broadcast(..., True))            
                if (message[:1] == '/'):
                    if (message[1:] == "start"): # and running == False):
                        print("TRYNA START")
                        running = True
                        # start a timer thread on new connect 
                        _thread.start_new_thread(_timer, (60,))
                    else:
                        broadcast(message[1:], conn, True)

                

                # broadcast chat messages to all users
                else:
                    # Calls broadcast function to send message to all but sender
                    br_message = "<" + addr[0] + "> " + message + "\n"
                    broadcast(br_message, conn, False) 

            else: 
                '''
                message may have no content if the connection is broken, 
                in this case we remove the connection
                '''
                remove(conn) 
  
        except: 
            continue
  
'''
Using the below function, we broadcast the message to all clients 
who's object is not the same as the one sending the message
'''
def broadcast(message, conn, isCommand): 
    # if recv'd a regular message -- broadcast
    if isCommand == False:
        for client in list_of_clients: 
            if client!=conn: 
                try: 
                    client.send(bytes(message, 'utf8'))
                except: 
                    # close and remove client
                    client.close() 
                    remove(client)

    # recv'd a command prepended with '/' -- only reply to sender
    else:
        for client in list_of_clients:
            if client == conn:
                serverReply = "Command not recognized\n"
                if message in commands:
                    serverReply = commands[message] + "\n"

                try:
                    client.send(bytes(serverReply, 'utf8'))
                except: 
                    # close and remove client
                    client.close() 
                    remove(client)


'''
The following function simply removes the object from the list that 
was created at the beginning of the program
'''
def remove(conn): 
    if conn in list_of_clients: 
        list_of_clients.remove(conn) 


def _timer(limit):
    start = time.time()
    end = time.time()
    curr = end - start
    while curr < limit:
        end = time.time()
    print("~~~ END OF TIMER ~~~")
    running = False


while 1: 

    '''
    Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected
    '''
    conn, addr = server.accept() 
  
    '''
    Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom
    '''
    list_of_clients.append(conn) 
  
    # prints and broadcasts the address of the user that just connected 
    print(addr[0] + " connected")
    connMessage = addr[0] + " connected" + "\n"
    
    for address in list_of_clients:
        broadcast(connMessage, address, False)
    
    # creates and individual thread for every user that connects  
    _thread.start_new_thread(clientthread, (conn,addr))


conn.close()
server.close()