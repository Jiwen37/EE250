# Lab 2

## Team Members
- Cynthia Liu
- Jiwen Li

## Lab Question Answers

Answer for Question 1: 
The reliability went down, and around half of the data was lost. We sent 30 digits, counting 1-10 three times, but only received 14 of them on the server. This occured because UDP does not have any mechanism to check whether all packages were received, so it just fires once and doesn't care about whether or not it was received. It is unable to detect package loss.

Answer for Question 2:
The reliability for TCP stayed the same: it was still reliable after the 50% loss was added. This is because TCP numbers the packages before sending so when the server receives the packages, if one of the numbers in the sequence is missing, it will check back with the client to make sure it receives the missing package.

Answer for Question 3:
The speed of TCP response decreased (slowed down) quite dramatically, because when packages are lost it takes time for the server to reach out to the client to get the package resent, causing delays. In addition, if the network is very busy, TCP will slow down package transmission to prevent overwhelming the network.

Answer for Question 4:
We used an LLM for help with code syntax for the socket library and for troubleshooting the rpi connection.

Answer for QC1:
argc stores the number of arguments that were input into the terminal when running the compiled code. If the number of arguments is less than 2, that means not enough arguments were provided for a port number to be provided, so it ends the code.
argv is where the arguments are stored. later in the code it references the first index of argv which makes sense because the second input in the terminal after calling for the compiled code is the port number.

Answer for QC2:
File descriptors provide an integer that uniquely identifies an open file socket or other open resources in a process. They are useful because it provides a consistent numbering system within the process. A file descriptor table is a table like structure that stores references to files, sockets, and other items that are open in the process.

Answer for QC3:
A struct is a datatype that stores a collection of variables/datatypes together. The sock address stores the server address and client address.

Answer for QC4:
The input parameters are AF_INET, SOCK_STREAM, 0, which correspond to communication domain, type of socket, and specific protocol, respectively.
The return value is -1 for an error and a non negative integer file descriptor otherwise

Answer for QC5:
The input parameters for bind() are the socket file descriptor, the address of the server, and the size of the server address (checks if the address length is less than zero)
The input parameter for listen() are the socket file descriptor, and the max number of client connections allowed

Answer for QC6:
Use while(1) because it runs forever and will continue to listen as long as there are no returns.
If the server can't connect to a new client, or can't read for a connection, there will be errors, and it will continue to close the connection. In the code, the server can only accept connections one at a time sequentially, so if there are multiple clients they have to wait until the ones before finish.

Answer for QC7:
fork() creates another process similar to the process that already exists for the new client (a child process), so now you have basically identical processes running at once, one for each client, so it can handle multiple clients at the same time.

Answer for QC8:
A system call is an interface between the script and the operating system's kernel, it is a request for the OS to perform privileged tasks that require user permission to be done.
