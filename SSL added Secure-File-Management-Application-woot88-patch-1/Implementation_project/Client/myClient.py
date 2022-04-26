# Plans for client
# User needs to be able to upload, download, and delete files from the server
# Add list function that list files on server.
# when sending always encode() and when recv always decode().
#
import socket
import sys
import os
import tqdm

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('Secure-File-Management-Application-woot88-patch-1/Implementation_project/Server/myServer.py')

# Variables for socket to use
TCP_connect = "127.0.0.1"  # loop back ip address
TCP_port = 7274  # Random tcp port number
BUFFER_SIZE = 2048  # Standard size
SEPARATOR = "<SEPARATOR>"  # Used to make uploading files easier

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
ssock = context.wrap_socket(sock, server_hostname=hostname)

# Handles connection to the server.
def connect():
    print("Attempting to establish connection with server")
    try:
        sock.connect((TCP_connect, TCP_port))
    except:
        print("Connection failed, either connection failed or wrong command (Im so sorry)")
    return


# Handles disconnection from server. Will probably add a way to close client as well since this shuts down the server
def disconnect():
    sock.send("disconnect".encode())
    # Wait for server go-ahead
    sock.recv(BUFFER_SIZE)
    sock.close()
    print("Server connection ended")
    return


# functions responsible for file management on server. (need to find out how server selects files)

# Test function to see if server receives commands properly
# Writes messages to be printed out by the server
def write():
    try:
        sock.send("write".encode())  # Sends command to server
        sock.recv(BUFFER_SIZE)  # Receives acknowledgement from server
        msg = input("enter text:")  # User inputs their message here
    except:
        print("Failed to send message. Check server status")
        return  # ends function upon failure
    try:
        sock.send(msg.encode())  # Sends user message to server
        return  # ends function
    except:
        print("\nStep 2 failed.")
        return  # ends function upon failure

# Download files from the server to the client
def download():
    try:
        # sends download command to server
        sock.send("download".encode())
    except:
        print("failed to send command check server")
        return
    # receives count from server.
    val = sock.recv(BUFFER_SIZE).decode('ascii')
    count = int(val)
    # Tells server its ready to receive file list
    sock.send("1".encode())
    while count > 0:
        print(sock.recv(BUFFER_SIZE).decode('ascii'))
        count -= 1
    try:
        filename = input("Enter the name of the file to download: ")
        sock.send(filename.encode())
    except:
        print("failed to verify file name from server")
        return
    try:
        user_data = sock.recv(BUFFER_SIZE).decode()
    except:
        print("Error receiving data from client")
        return
    filename, filesize = user_data.split(SEPARATOR)
    # remove file path if there is one
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the server
    progress = tqdm.tqdm(range(filesize), f"Receiving{filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
            while True:
                print("receiving data...")
                # read 1024 bytes from the server (receive)
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    print("File download {} complete".format(filename))
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                progress.update(len(bytes_read))
    sock.close()

def delete():
    try:
        # sends download command to server
        sock.send("delete".encode())
    except:
        print("failed to send command check server")
        return
    # receives count from server.
    val = sock.recv(BUFFER_SIZE).decode('ascii')
    count = int(val)
    # Tells server its ready to receive file list
    sock.send("1".encode())
    while count > 0:
        print(sock.recv(BUFFER_SIZE).decode('ascii'))
        count -= 1
    filename = input("Enter the name of the file to delete ")
    sock.send(filename.encode())
    print(sock.recv(BUFFER_SIZE).decode('ascii'))
    return

#  Uploads file to the location of the server
def upload():
    print("choose a file to upload")
    for name in os.listdir():
        if not name.endswith(".py"):
            print(name)
    try:
        sock.send("upload".encode())
        sock.recv(BUFFER_SIZE)
        filename = input("Enter the name of the file to upload: ")
    except:
        print("failed to send command. Check connection to server\n")
        return
    # gets size of file
    filesize = os.path.getsize(filename)
    try:
        # Sends filename and Size to the server.
        sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
    except:
        print("File failed to send. Check connection")
    progress = tqdm.tqdm(range(filesize),f"Sending{filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                print("File transmission complete")
                break
            sock.sendall(bytes_read)
            # updates progress bar
            progress.update(len(bytes_read))
    sock.close()

while True:
    print("Currently there are 5 commands that are Usable\n"
          + "   connect: connects to the server \n"
          + "disconnect: disconnects from the server\n"
          + "     write: prints text to the screen of the server\n"
          + "    upload: Uploads a file from the folder the clients application is located\n"
          + "  download: Downloads a file from the folder the server application is located\n"
          + "    delete: Deletes a file from the server folder.")
    prompt = input("Enter command:")
    # Nested if else that reads prompt for commands
    if prompt == "connect":
        connect()
    elif prompt == "disconnect":
        disconnect()
    elif prompt == "write":
        write()
    elif prompt == "quit":
        break
    elif prompt == "upload":
        upload()
        break
    elif prompt == "download":
        download()
        break
    elif prompt == "delete":
        delete()
        break
    else:
        print("command not recognised:{}".format(prompt))
