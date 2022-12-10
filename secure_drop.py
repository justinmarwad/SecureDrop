#!/usr/bin/env python3

import argparse, requests, json
from getpass import getpass

class Client: 
    """ Main client code..."""
    def __init__(self, email, server="http://localhost:8000", lport=9999):
        self.email=email
        self.server=server
        self.lport=lport

        self.name=""
        self.passwd=""
        self.pubkey="asdasd"  
        self.logged_in=False 

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

        self.name = input("Enter your name: ")
        self.email = input("Enter your email: ")
        self.passwd = getpass()

        data = {"email": self.email, "name": self.name, "passwd": self.passwd, "pubkey": self.pubkey}

        response = requests.post(f"{self.server}/register", data=data, verify=False)

        if response.status_code == 201: 
            print("[+] INFO | User created successfully.")

    def login(self, passwd): 
        """ Method to login to the server. Argument passwd accepts string of password.""" 

        response = requests.post(f"{self.server}/login", data={"email":self.email,"passwd": self.passwd}, verify=False)

        if response.status_code == 200:
            response = response.json()
            if response["login"] == "True": 
                print("[+] INFO | Login successful.")
                self.logged_in=True
            
    def list_users(self): 
        """ Method to list all online users.""" 
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
    client = Client(email=args["email"]) 
        
    # client.setup()
    # client.login()

    if args["add"]: 
        client.create_user()
    elif args["list"]:
        client.list_users() 
    elif args["send"]:
        client.communicate()
    

