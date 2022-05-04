# Secure-File-Management-Application
IS-3033 Class Project Repository 

## Functionality
Verion 1.0.1 

Connection isolated to local machine

IP: 127.0.0.1

Port: 7274 
 
### Commands 
  
  * upload: uploads file to server then closes server
  
  * download: downloads file from server then closes 
  
  * write: Prints out message on server  //used for testing purposes should remove later

  * delete: Delete's files from the server

So far message.txt and Other_File.txt are used to test if the client and server can transfer files. 

## Issues
Server crashes if commands are intrupted mid way. 

log deletes self everytime server is restarted.

client has to restart every time a command is entered.



# TO DO
1. Add exceptions to make sure commands dont crash server when being used mid process.
2. fix log file deleting itself every time the server restarts.
3. add fancy login for client. 
4. finish this list.
