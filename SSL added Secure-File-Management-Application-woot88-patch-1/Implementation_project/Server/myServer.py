# use socket listen to specify the number of connections allowed at once.
# Need to find what imports to add
# Pretty sure logging is going to take place on this application
# encode and decode are essential to any type of communication
import socket
import os
import tqdm

def process_command():
    import socket
import ssl

hostname = '127.0.0.1'
context = ssl.create_default_context()

sock = socket.create_connection((hostname, 443)):
    ssock = context.wrap_socket(sock, server_hostname=hostname):

hostname = '127.0.0.1'
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('Secure-File-Management-Application-woot88-patch-1/Implementation_project/Client')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0):
    ssock context.wrap_socket(sock, server_hostname=hostname):

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('Secure-File-Management-Application-woot88-patch-1/Implementation_project/Client')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0):
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)
    ssock = context.wrap_socket(sock, server_side=True):
        conn, addr = ssock.accept()
        ...

# Variables for socket to use.
TCP_connect = "127.0.0.1"  # set to loop back for internal server testing purposes. add real ip's later.
TCP_port = 7274  # Random tcp port number
BUFFER_SIZE = 2048  # Standard size
SEPARATOR = "<SEPARATOR>"  # Used to make uploading files easier



# Handles the disconnection process and shuts server down
def disconnect():
    # Tells the client it's ready to disconnect.
    conn.send("1".encode())
    # Closes the clients connection
    conn.close()
    sock.close()
    print("client disconnected\n")
    return


# Prints message received from clients.
def write():
    # Tells the client it's ready to accept messages
    conn.send("1".encode())
    # Turns the received message to ascii string
    msg = conn.recv(BUFFER_SIZE).decode('ascii')
    print(msg)
    return

# Receives file from client and adds file to folder application is stored in.
def upload():
    #  Tells the client it's ready to receive files
    conn.send("1".encode())
    #  Data user has uploaded form the client socket
    try:
        user_data = conn.recv(BUFFER_SIZE).decode()
    except:
        print("Error receiving data from client")
        return
    filename, filesize = user_data.split(SEPARATOR)
    # remove file path if there is one
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(BUFFER_SIZE)
            if not bytes_read:
                print("File upload {} complete".format(filename))
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    conn.close()

# Sends a file to the client from the server
def download():
    # counts the number of files in the directory
    count = 0
    for name in os.listdir():
        if not name.endswith(".py"):
            count += 1
    val = str(count)
    # sends number of files in server directory to client.
    conn.send(val.encode())
    # Gets ok from client to start sending file list
    conn.recv(BUFFER_SIZE)
    # sends file name to client in a list.
    for name in os.listdir():
        if not name.endswith(".py"):
            conn.send(name.encode())
    #  Data user has uploaded form the client socket.
    try:
        filename = conn.recv(BUFFER_SIZE).decode('ascii')
    except:
        print("failed to verify file name")
    # gets size of file
    filesize = os.path.getsize(filename)
    try:
        # Sends filename and Size to the client
        conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
    except:
        print("File failed to send. Check connection.")
        return
    progress = tqdm.tqdm(range(filesize), f"Sending{filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            conn.send(bytes_read)
            if not bytes_read:
                print("File transmission complete")
                break
            # updates progress bar
            progress.update(len(bytes_read))
    conn.close()
    sock.close()

def delete():
    # counts the number of files in the directory
    count = 0
    for name in os.listdir():
        if not name.endswith(".py"):
            count += 1
    val = str(count)
    # sends number of files in server directory to client.
    conn.send(val.encode())
    # Gets ok from client to start sending file list
    conn.recv(BUFFER_SIZE)
    # sends file name to client in a list.
    for name in os.listdir():
        if not name.endswith(".py"):
            conn.send(name.encode())
    # Receives file requested for deletion from client.
    try:
        filename = conn.recv(BUFFER_SIZE).decode('ascii')
    except:
        print("failed to receive name of file")
        return
    # Checks if the file path is real or not.
    if os.path.isfile(filename):
        os.remove(filename) # removes file
    else:
        print("Error: check name of file")
    return

# Waits for commands and processes them
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Opens server connection and stores connection info.
    sock.bind((TCP_connect, TCP_port))  # Connection that is attached to the server.
    sock.listen(1)  # Number of connections allowed in the server
    print("listening for connections...\n")  # added to confirm is server was running
    conn, address = sock.accept()  # accepts connections and appends them to conn, and address.
    print("Connection established by {}".format(address))

    print("\nwaiting for commands\n")
    data = conn.recv(BUFFER_SIZE).decode('ascii')
    print(data)
    # Nested if that selects which command to run based off of user input
    if data == "write":
        print("writing message...\n")
        write()
    elif data == "disconnect":
        disconnect()
        break
    elif data == "upload":
        upload()
        break
    elif data == "download":
        download()
        break
    elif data == "delete":
        delete()
        break
    # if a command is not recognized it will get reset and loop
    data = None
