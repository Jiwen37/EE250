# Lab 9 Writeup
## Cynthia Liu, Jiwen Li

### What type of authentication are we using here (currently)? Does it use any keys?
We are using username/password authentication. Keys are not used for the authentication, they are used later for the encryption.

### Both TLS (encryption) and crypto authentication use public-private key pairs. For TLS encryption what keys are used when the client sends a message to the server? For crypto authentication, explain how the server can verify a message is from a given client?
In TLS encryption, a shared symmetric session key is used when the client sends a message to the server. The public and private keys are used to initially establish a secure connection. In crypto authentication, the client sends a message with its private key

### Here we created a pair of asymmetric keys. What are their names? Which one is the public key and which one is the private key?

### What is a certificate authority (CA) for public keys? What kind of attack can a CA prevent?
