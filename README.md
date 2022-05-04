# Secure-File-Management-Application
IS-3033 Class Project Repository 

## Functionality
Verion 1.0.0 

Should only use local machine for connection 

IP: 127.0.0.1

Port: 7274 
 
### Commands 
  
  * upload: uploads file to server then closes server
  
  * download: downloads file from server then closes 
  
  * write: Prints out message on server  //used for testing purposes should remove later

  * delete: Delete's files from the server

So far message.txt and Other_File.txt are used to test if the client and server can transfer files. 

## Logging
When a user attempts to login with invalid credentials this will append the connection to the log. 

All commands and user's along with their UID's will be logged. 
Thier ability to execute the command will also be logged. 

Finally for whatever reason the log file will reset every time the server is reset.
I currently do not know how to fix this. 

## Current Issues
Client has to restart every time a command is entered.

Log will reset every time the server is rerun and will not save.

Commands will crash server if not entered in expected order (try to add exceptions for simple user mistakes like adding a space?)

There is no max login attempts at the moment.

# TO Do
1. Implement Muletti's login funciton to the client if possible. 
2. find more places the program can go wrong and add excpetions where needed 
3. complete this list.
