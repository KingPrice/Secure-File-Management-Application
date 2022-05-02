# Plans for client
# User needs to be able to upload, download, and delete files from the server
# Add list function that list files on server.
# when sending always encode() and when recv always decode().
#
import socket
import os
import tqdm
import ssl



# Variables for socket to use
BUFFER_SIZE = 1024  # Standard size
SEPARATOR = "<SEPARATOR>"  # Used to make uploading files easier
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SSL variables here
WSock = ssl.wrap_socket(sock, keyfile="Certs/ImpDemo.key", certfile="Certs/ImpDemo.crt")

# Handles connection to the server.
def connect(TCP_connect = '127.0.0.1', TCP_port = 7274):
    print("Attempting to establish connection with server")
    try:
        WSock.connect((TCP_connect, TCP_port))
    except:
        print("Connection failed, either connection failed or wrong command (Im so sorry)")
    print("Connection established")


"""
# Handles disconnection from server. Will probably add a way to close client as well since this shuts down the server
def disconnect():
    sock.send("disconnect".encode())
    # Wait for server go-ahead
    sock.recv(BUFFER_SIZE)
    sock.close()
    print("Server connection ended")
    return
"""

# functions responsible for file management on server. (need to find out how server selects files)

# Test function to see if server receives commands properly
# Writes messages to be printed out by the server (REMOVE LATER)
def write():
    try:
        WSock.send("write".encode())  # Sends command to server
        msg = input("enter text:")  # User inputs their message here
    except:
        print("Failed to send message. Check server status")
        return  # ends function upon failure
    try:
        WSock.send(msg.encode())  # Sends user message to server
        return  # ends function
    except:
        print("\nStep 2 failed.")
        return  # ends function upon failure


# Download files from the server to the client
def download():
    try:
        # sends download command to server
        WSock.send("download".encode())
    except:
        print("failed to send command check server")
        return
    # receives count from server.
    val = WSock.recv(BUFFER_SIZE).decode('ascii')
    count = int(val)
    # Tells server its ready to receive file list
    WSock.send("1".encode())
    # list files that can be downloaded on the client
    while count > 0:
        print(WSock.recv(BUFFER_SIZE).decode('ascii'))
        count -= 1
    # Sends file to server
    try:
        filename = input("Enter the name of the file to download: ")
        WSock.send(filename.encode())
    except:
        print("failed to verify file name from server")
        return
    # Receives file name and size
    try:
        user_data = WSock.recv(BUFFER_SIZE).decode()
    except:
        print("Error receiving data from client")
        return
    # removes file SEPARATOR from user_data
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
            bytes_read = WSock.recv(BUFFER_SIZE)
            if not bytes_read:
                print("File download {} complete".format(filename))
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            progress.update(len(bytes_read))
    WSock.close()


# command that handles file deletion
def delete():
    try:
        # sends download command to server
        WSock.send("delete".encode())
    except:
        print("failed to send command check server")
        return
    # receives count from server.
    val = WSock.recv(BUFFER_SIZE).decode('ascii')
    count = int(val)
    # Tells server its ready to receive file list
    WSock.send("1".encode())
    # As long as the number of files is higher than 0 List them on client.
    while count > 0:
        print(WSock.recv(BUFFER_SIZE).decode('ascii'))
        count -= 1
    # Sends the file requested to be deleted
    filename = input("Enter the name of the file to delete ")
    WSock.send(filename.encode())
    print(WSock.recv(BUFFER_SIZE).decode('ascii'))
    # Verification of file deleted
    print("File has been deleted")
    return


#  Uploads file to the location of the server
def upload():
    print("choose a file to upload")
    for name in os.listdir():
        if not name.endswith(".py"):
            print(name)
    try:
        WSock.send("upload".encode())
        WSock.recv(BUFFER_SIZE)
        filename = input("Enter the name of the file to upload: ")
    except:
        print("failed to send command. Check connection to server\n")
        return
    # gets size of file
    filesize = os.path.getsize(filename)
    try:
        # Sends filename and Size to the server.
        WSock.send(f"{filename}{SEPARATOR}{filesize}".encode())
    except:
        print("File failed to send. Check connection")
    progress = tqdm.tqdm(range(filesize), f"Sending{filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                print("File transmission complete")
                break
            WSock.sendall(bytes_read)
            # updates progress bar
            progress.update(len(bytes_read))
    WSock.close()


while True:
    sel = input("Would you like to use default address y/n?:  ")
    if sel == 'y':
        connect()
    else:
        TCP_connect = input("Enter ip address:  ")
        TCP_port = int(input("Enter a portnumber"))
        connect(TCP_connect, TCP_port)


    print("Currently there are 4 commands that are Usable\n"
          + "     write: prints text to the screen of the server\n"
          + "    upload: Uploads a file from the folder the clients application is located\n"
          + "  download: Downloads a file from the folder the server application is located\n"
          + "    delete: Deletes a file from the server folder.")
    prompt = input("Enter command:")
    # Nested if else that reads prompt for commands
    if prompt == "write":
        write()
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
