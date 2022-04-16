# use socket listen to specify the number of connections allowed at once.
# Need to find what imports to add
# Pretty sure logging is going to take place on this application
# encode and decode are essential to any type of communication
import sys
import socket

from serCommands import *

def process_command():
    conn, addr = sock.accept() # Should be ready to read
    print(f"Accepted connection from {addr}")
    cmd = conn.recv(1024).decode('ascii')
    if(cmd == "upload"):
        upload(conn)
    elif(cmd == "download"):
        download(conn)
    elif(cmd == "delete"):
        delete(conn)
    elif(cmd == "write"):
        write(conn)
    else:
        print("Error please enter a valid command")
    return



if len(sys.argv) != 3:
    host = input("Enter ip address to host:  ")
    port = input("Enter port number:  ")
    port = int(port)
else:
    host, port = sys.argv[1], int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen()
print(f"Listening on {(host, port)}")

try:
    while True:
        process_command()
except KeyboardInterrupt as e:
    print("Closing test server program")



