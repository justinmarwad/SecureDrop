#!/usr/bin/env python3

import argparse, requests, json
from getpass import getpass
from Crypto.PublicKey import RSA
from base64 import b64decode,b64encode
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


class Client: 
    """ Main client code..."""
    def __init__(self, email, server="http://localhost:8000", lport=9999):
        self.email=email
        self.server=server
        self.lport=lport

        self.name=""
        self.passwd=""
        self.pubkey=""  
        self.pubkey=""  
        self.logged_in=False 

    def get_user_info(self):
        """ Method to get user information from a file. """
        
        try: 
            with open("user_info.json", "r") as f:
                user_info = json.load(f)

            self.email = user_info["email"]
            self.name = user_info["name"]
            self.passwd = user_info["passwd"]
            self.pubkey = user_info["pubkey"]
            self.privkey = user_info["privkey"]

            return True 

        except FileNotFoundError: 
            return False

    def save_user_info(self):
        """ Method to save user information to a file. """
        
        with open("user_info.json", "w") as f:
            json.dump({
                "email": self.email, 
                "name": self.name, 
                "passwd": self.passwd, 
                "pubkey": self.pubkey,
                "privkey": self.privkey
            }, f)

    def generate_keys(self):
        """ Method to generate a new RSA key pair. """

        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

        self.privkey = private_key.decode()
        self.pubkey = public_key.decode()

    def create_user(self): 
        """ Method to create a brand new user. """ 

        print("[+] INFO | Please create a new user account below: ")

        self.name = input("Enter your name: ")
        self.email = input("Enter your email: ")
        self.passwd = getpass()

        # generate a new RSA key pair
        self.generate_keys() 

        data = {
            "email": self.email, 
            "name": self.name, 
            "passwd": self.passwd, 
            "pubkey": self.pubkey,
            "privkey": self.privkey
        }

        print(data)

        response = requests.post(f"{self.server}/register", data=data, verify=False)

        if response.status_code == 201: 
            print("[+] INFO | User created successfully.")
            self.save_user_info()

    def login(self): 
        """ Method to login to the server. Argument passwd accepts string of password.""" 

        print("[+] INFO | Please login below: ")

        # If email & pass not provided by cli, then ask for it 
        if not self.email:
            self.email = input("Enter your email: ")
        if not self.passwd: 
            self.passwd = getpass()

        # Send login request to server
        response = requests.post(f"{self.server}/login", data={"email":self.email,"passwd": self.passwd}, verify=False)

        if response.status_code == 200:
            response = response.json()
            if response["login"] == "True": 
                print("[+] INFO | Login successful.")

                # download pub and priv key 
                self.pubkey = response["pubkey"]
                self.privkey = response["privkey"]

                # save creds to device
                self.save_user_info() 

            else: 
                print("[-] ERROR | Login failed or account not found. Please try again or create a new account.")
            
    def list_users(self): 
        """ Method to list all online users.""" 
        print(f"Logged in! {self.email} {self.name} {self.passwd} {self.pubkey}") 

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
        
    # login user in if they have creds saved 
    client.get_user_info()

    if args["email"]: 
        client.login()
    elif args["add"]: 
        client.create_user()
    elif args["list"]:
        client.list_users() 
    elif args["send"]:
        client.communicate()
    

