# Secure-File-Management-Application
IS-3033 Class Project Repository 

### Functionality ###
Verion 0.0.2 Alpha

So far only uses local connection on machine. 
IP: 127.0.0.1
Port: 7274 
 
There are only 5 commands out of 6 which are still missing implementation

   connect: connects to server
   
disconnect: closes and shuts server down

    upload: uploads file to server then closes server

  download: downloads file from server then closes 

     write: Prints out message on server //used for testing purposes should remove later

So far message.txt is just used to be transfered from client to server.

### TO DO ###
1. Add Delete command.
2. Fix client and server closing after running a command (write is exempt from this)
3. Make commands much more robust so they do not break when user misinputs.
4. Remove write once all other commands are properly implemented.
5. add OPENLDAP functionality. 
6. complete this list.
