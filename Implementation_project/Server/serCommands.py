
import os
import tqdm
import ldap

# Figure a way to implement this like a switch statement because the coding on this gets redundant very fast
# And it's super annoying. Also, it may make it easier to implement ldap and other things with this doc just
# being used for commands

SEPARATOR = "<SEPARATOR>"
def login(conn):
    ldapconn = ldap.initialize('ldap://localhost')

    ID = ""

    cn = conn.recv(1024).decode("utf-8")
    User = 'cn=' + cn + ',cn=SysUsers,dc=ImpDemo,dc=com'
    PW = conn.recv(1024).decode("utf-8")
    ldapconn.simple_bind_s(User, PW)
    cn = 'cn=' + cn
    UID = ldapconn.search_s("dc=ImpDemo,dc=com", ldap.SCOPE_SUBTREE, cn, ['uidNumber'])
    UID = str(UID)
    for n in UID:
        if n.isdecimal():
            ID = ID + n
    return ID

# Prints message received from clients. LMAO everyone can use this
def write(conn):
    # Turns the received message to ascii string
    msg = conn.recv(1024).decode("utf-8")
    print(msg)

    conn.close()
    return


# Receives file from client and adds file to folder application is stored in.
def upload(conn,perms):
    if perms == '1000' | '1002':
        #  Tells the client it's ready to receive files
        conn.send("1".encode())
        #  Data user has uploaded form the client socket
        try:
            user_data = conn.recv(1024).decode()
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
        # opens file and begins to write the file to the server folder
        with open('files/' + filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = conn.recv(1024)
                if not bytes_read:
                    print("File upload {} complete".format(filename))
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
    else:
          # Add error log saying user invalid


# Sends a file to the client from the server
def download(conn,perms):
    # Elias and Bob can download files
    if perms == '1000' | '1001':
        # counts the number of files in the directory
        count = 0
        # counts file in directory. Does not count the server file.
        for name in os.listdir('files'):
            if not name.endswith(".py"):
                count += 1
        val = str(count)
        # sends number of files in server directory to client.
        conn.send(val.encode())
        # Gets ok from client to start sending file list
        conn.recv(1024)
        # sends file name to client in a list.
        for name in os.listdir('files'):
            if not name.endswith(".py"):
                conn.send(name.encode())
        #  Data user has uploaded form the client socket.
        try:
            filename = conn.recv(1024).decode('ascii')
        except:
            print("failed to verify file name")
        # gets size of file
        filesize = os.path.getsize('files/' + filename)
        try:
            # Sends filename and Size to the client
            conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
        except:
            print("File failed to send. Check connection.")
            return
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        # opens file in server and begins to write it to file.
        with open('files/' + filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(1024)
                conn.send(bytes_read)
                if not bytes_read:
                    print("File transmission complete")
                    break
                # updates progress bar
                progress.update(len(bytes_read))
        conn.close()
    else:
          # enter invalid user here
        #sock.close()

def delete(conn,perms):
    if perms == '1002':
        # counts the number of files in the directory
        count = 0
        for name in os.listdir('files'):
            if not name.endswith(".py"):
                count += 1
        val = str(count)
        # sends number of files in server directory to client.
        conn.send(val.encode())
        # Gets ok from client to start sending file list
        conn.recv(1024)
        # sends file name to client in a list.
        for name in os.listdir('files'):
            if not name.endswith(".py"):
                conn.send(name.encode())
        # Receives file requested for deletion from client.
        try:
            filename = conn.recv(1024).decode('ascii')
        except:
            print("failed to receive name of file")
            return
        # Checks if the file path is real or not.
        if os.path.isfile('files/' + filename):
            os.remove('files/' + filename) # removes file
            print("File deleted")
        else:
            print("Error: check name of file")
    else:
          # Enter invalid user here

