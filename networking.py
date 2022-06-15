import socket

############ SERVER #############

# create a socket object
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    msg = 'Thank you for connecting' + "\r\n"
    clientsocket.send(msg.encode('ascii'))
    clientsocket.close()

############ CLIENT #############

# create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = clientSocket.gethostname()

port = 9999

# connection to hostname on the port.
clientSocket.connect((host, port))

# Receive no more than 1024 bytes
msg = clientSocket.recv(1024)

clientSocket.close()
print(msg.decode('ascii'))
