#!/usr/bin/env python3

import argparse

class Client: 
    """ Main client code..."""
    def __init__(self, email, server="https://localhost", lport=9999):
        self.email=email
        self.pub_key=""  
        self.server=server
        self.lport=lport

    def setup(self): 
        """ Method to setup the client. """
        # Step 1: Check if user information is saved to device, go directly to step 3 if so 
        #
        # Step 2: Check if email exists on the server, if so, then login, else create a new user.
        # 
        # Step 3: Save user information to a file.
        # 
        # Step 4: Set the self.pub_key variable to the user's public key (create if it doesn't exist).            
        pass

    def create_user(self): 
        """ Method to create a brand new user. """            
        pass 

    def login(self): 
        """ Method to login to the server. """            
        pass 

    def communicate(self): 
        """ Method to PEER-to-PEER communicate with other clients. """            
        pass


if __name__ == "__main__": 
    # Arg Parser code 
    parser = argparse.ArgumentParser(description="Secure Drop Client")
    parser.add_argument("-a", "--add", help="Create new user", action='store_true')
    parser.add_argument("-l", "--list", help="List online users", action='store_true')
    parser.add_argument("-s", "--send", help="Send file to user", action='store_true')
    parser.add_argument("-e", "--email", help="Provide an email")
    parser.add_argument("-f", "--file", help="Provide a file")
    args = vars(parser.parse_args())
    
    # Client code 
    client1 = Client(email=args["email"]) 
