
import sys
import socket
import ssl

from serCommands import *

def process_command():
    conn, addr = WSock.accept() # Should be ready to read
    print(f"Accepted connection from {addr}")
    perms = login(conn, addr) #add error handling
    cmd = conn.recv(1024).decode('ascii')
    if(cmd == "upload"):
        upload(conn, perms)
    elif(cmd == "download"):
        download(conn, perms)
    elif(cmd == "delete"):
        delete(conn, perms)
    elif(cmd == "write"):
        write(conn, perms)
    else:
        print("Error please enter a valid command")
    return

# If server is not feed connection info will use default connection.
if len(sys.argv) != 3:
    host = '127.0.0.1'
    port = 7274
else:
    host, port = sys.argv[1], int(sys.argv[2])

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Wrapper setup
WSock = ssl.wrap_socket(
    sock, server_side=True, keyfile="Certs/ImpDemo.key", certfile="Certs/ImpDemo.crt"
)

WSock.bind((host, port))
WSock.listen()
print(f"Listening on {(host, port)}")

# try statement that runs commands and closes if keyboardInterrupt is sent.
try:
    while True:
        process_command()
except KeyboardInterrupt as e:
    print("Closing test server program")



