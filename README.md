# Secure-File-Management-Application
IS-3033 Class Project Repository 

## Functionality
Verion 0.1.3 Alpha

So far only uses local connection on machine. 

IP: 127.0.0.1

Port: 7274 
 
### Commands 
  * connect: connects to server
  
  * disconnect: closes and shuts server down
  
  * upload: uploads file to server then closes server
  
  * download: downloads file from server then closes 
  
  * write: Prints out message on server  //used for testing purposes should remove later

  * delete: Delete's files from the server

So far message.txt is just used to be transfered from client to server.

Added LDAP part but it does not work yet
# TO DO
1. Fix client and server closing after running a command (write is exempt from this)
2. Make commands much more robust so they do not break when user misinputs.
3. Remove write once all other commands are properly implemented.
4. add OPENLDAP functionality. 
5. complete this list.
