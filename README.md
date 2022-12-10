# SecureDrop 

## Table of Contents

- [SecureDrop](#securedrop)
  - [Table of Contents](#table-of-contents)
  - [1 Project Overview](#1-project-overview)
    - [1.1 Introduction](#11-introduction)
    - [1.2 Project Milestones](#12-project-milestones)
      - [1.2.1 Milestone 1: User Registration](#121-milestone-1-user-registration)
      - [1.2.2 Milestone 2: User Login](#122-milestone-2-user-login)
      - [1.2.3 Milestone 3: Adding Contacts](#123-milestone-3-adding-contacts)
      - [1.2.4 Milestone 4: Listing Contacts](#124-milestone-4-listing-contacts)
      - [1.2.5 Milestone 5: Secure File Transfer](#125-milestone-5-secure-file-transfer)
  - [2 Project Explained](#2-project-explained)
    - [2.1 Plan](#21-plan)
    - [2.1 How It Works](#21-how-it-works)
      - [2.1.1 User Registration](#211-user-registration)
      - [2.1.2 User Lookup](#212-user-lookup)
      - [2.1.2 CA](#212-ca)
- [Authors](#authors)
- [License](#license)


## [1 Project Overview](#1-project-overview) 

### [1.1 Introduction](#11-introduction)  

The objective of this project is to introduce you to cryptographic tools via the implementation of a secure file transfer protocol. Your implementation will be similar to and a subset of a very popular tool used in Apple devices, called AirDrop. During the process, you will practice many cryptographic and cybersecurity concepts such as symmetric and asymmetric cryptography, digital certificates, public key infrastructure, mutual authentication, non-repudiation, confidentiality, integrity protection and password security.

### [1.2 Project Milestones](#12-project-milestones)

#### [1.2.1 Milestone 1: User Registration](#121-milestone-1-user-registration)

Keep in mind the following points when implementing the module -

1. You are not expected to implement databases for storing the information, and simple files / JSON
structures should work.
2. Implement the module first without any security controls. Once the module has been tested to work
correctly, implement the security controls. Focus on simple controls that can protect against traditional
password cracking attacks.
3. Write reusable code. The password security implementation can also be reused for the User Login
milestone.
4. Use third party APIs. The Python crypt module can be very helpful if you plan to implement salted
hashes for password security.
5. Think about what information will be required for mutual authentication in the next milestones.
Generate and save the information during the registration process. If you plan to use digital certificates for mutual authentication, you can assume that a CA is present on all the clients. Generate a CA
manually for testing purposes.

#### [1.2.2 Milestone 2: User Login](#122-milestone-2-user-login)

This is a simple milestone that can be implemented quickly. Keep in mind the following points when
implementing the module -

1. Write reusable code. Much of the code will be similar to the User Registration milestone. It will save
you a lot of time.
2. Think about how you can use information from the login credentials to enhance security in the next
milestones. Generate and keep the information in memory. Remember that keeping the password in
memory is not recommended. All other information must be forgotten when the user exits the program


#### [1.2.3 Milestone 3: Adding Contacts](#123-milestone-3-file-transfer)

This is also a simple module that can be implemented quickly. Keep in mind the following points when
implementing the module -

1. You are not expected to implement databases for storing the information, and simple files / JSON
structures should work. You can assume that each user will have limited number of contacts and there
is no need to develop algorithms and data structure to efficiently store and retrieve contacts.

2. Think about how you can use the information generated in milestone 2 to ensure the confidentiality and integrity of the contact information. An attacker who gains access to your client should not be able to
access the contact information. Any changes made by the attacker should get automatically detected.
A compromise of contact information can easily lead to spam and targeted attacks on those contacts.

#### [1.2.4 Milestone 4: Listing Contacts](#124-milestone-4-file-transfer)

This is a tricky milestone that will require careful design and implementation. This is the first time the
application communicates over the network. As such, the applications’s attack surface is significantly increased.
Keep in mind the following points when implementing the module -

1. Remember that a contact information should only display if the user has added them as a contact, the contact has also added the user as their contact, and the contact is online on the same network. 
2. Implement the module first without any security controls. Once the module has been tested to work correctly, implement the security controls. Do not implement the transport layer protocols and use TCP or UDP. The Python socket module contains easy-to-use implementations of transport layer protocols.
3. Write reusable code, at least, for code that performs cryptographic operations. The Python PyCrypto
and cryptography modules can be very helpful in implementing the many different cryptographic operations. These implementations can be reused for the Secure File Transfer milestone.
4. Ensure that the identities of the communicating entities are encrypted. An attacker sniffing packets on
your network should not be able to obtain the email addresses of the contacts. As mentioned earlier, a
compromise of the contact information can easily lead to spam and targeted attacks on your contacts.
5. Think about how you can mitigate impersonation attacks. The attacker can pose both as a sender or a
receiver in the communication. This threat can be avoided by implementing a protocol that performs
mutual authentication between the communicating entities.
6. Think about any information that can be exchanged between the entities to enhance the security of the
next step, and help avoid re-perfoming the mutual authentication. This information must be unique to
the communication and protected from the attacker. Compromise of the information should not result
in a compromise of the file transfer

#### [1.2.5 Milestone 5: Secure File Transfer](#125-milestone-5-secure-file-transfer)

The complexity of this milestone depends on the design of the previous milestone. Keep in mind the following
points when implementing the module -

1. Think about how you can efficiently transmit large files without compromising the confidentiality and
integrity of the file. The received file must be exactly the same as the transmitted file. The system
must ensure this before notifying the user of successful transfer.
2. Think about how you can mitigate replay attacks. The attacker who has recorded a previous communi-
cation must not be able to replay the communication to send / receive files. This threat can typically
be avoided by using incremental sequence numbers starting with a random seed on every client.


## [2 Project Explained](#2-project-explained)

### [2.1 Plan](#21-plan) 


1. Create persistent way to save login information (run a database with a Django server perhaps?)

2. Add five new commands to the client (help, add, list, send, and exit)

3. 


### [2.1 How It Works](#21-how-it-works) 


#### [2.1.1 User Registration](#211-user-registration)

1. Send a post request to ```http://localhost:8000/register``` with the json ```{"email": "<the_email>", "name": "<the_name>", "passwd": "<the_password>", "pubkey": "<the_pubkey>"}```

#### [2.1.2 User Lookup](#212-user-lookup)

1. Send a post request to this url ```http://localhost:8000/lookup``` with the json ```{"email": "<the_email>"}``` 

#### [2.1.2 CA](#212-ca)

Steps to generate CA and server certificate: 

```bash
sudo apt install easy-rsa -y
/usr/share/easy-rsa/easyrsa init-pki
/usr/share/easy-rsa/easyrsa build-ca nopass # ca name: ca.securedrop.local
/usr/share/easy-rsa/easyrsa gen-req securedrop.local nopass
/usr/share/easy-rsa/easyrsa import-req pki/reqs/securedrop.local.req securedropp.local
/usr/share/easy-rsa/easyrsa sign-req server securedropp.local

# Create final pem key with ca key and server crt
cat pki/issued/securedrop.local.crt pki/private/securedrop.local.key > pki/issued/securedrop.local.pem
```

# Authors

- Chris 
- Justin Marwad 

# License 

Copyright 2022 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.