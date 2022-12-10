import socket, requests, json, ssl, json, random   
import os, string, multiprocessing, signal
from colorama import Fore, Style
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## OUR CLIENT CODE ## 
class Client: 
    """ Main client code..."""
    def __init__(self, name="Rick_Astley", server="https://127.0.0.1:5000", port=9090): 
        self.name=name
        self.pub_key=f"public-{''.join(random.choices(string.ascii_lowercase, k=5))}.crt"
        self.priv_key=f"private-{''.join(random.choices(string.ascii_lowercase, k=5))}.key"

        self.port=port  
        self.server=server 

        self.clients=[]
        self.connected_clients=[]

        self.create_keys()
        self.get_client_list()

    def __del__(self):
        self.delete_keys()

    def create_keys(self): 
        """ Method to create keys """ 
        output=os.popen(f"openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout {self.priv_key} -out  {self.pub_key} -subj '/CN=rick.local/'").read() 
        print(Fore.GREEN + output + Style.RESET_ALL)

    def delete_keys(self):
        """ Delete all keys. Run this method on exit please."""
        print(Fore.GREEN + os.popen(f"rm {self.priv_key} {self.priv_key}")  + Style.RESET_ALL)

    def get_local_ip(self): 
        """ Returns the local ip address as a string.""" 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return(s.getsockname()[0])

    def get_client_list(self): 
        """ Method to get a list of clients from the server. """            

        with open(self.pub_key, "rb") as f:
            pub_key_text = f.read().decode("utf-8") 

        response = requests.post(self.server, data=json.dumps({
            "client_name": self.name, 
            "client_ip": self.get_local_ip(),
            "public_key": pub_key_text,
        }), verify=False)

        if response.status_code == 200: 
            self.clients = json.loads(response.content)["clients"]

            # for client in self.clients:
            #     print(Fore.GREEN + f"[+] INFO | Found {client['client_name']}@{client['client_ip']}" + Style.RESET_ALL)

        else:
            raise Exception(f"[ERROR] Could not recieve information from the server {self.server}.")

         
    def send(self, message="ping!"): 
        """ Method to send message to another client. """

        while True:
            for client in self.clients: 
                                                   

                client_pub_key = f"read-{self.pub_key}"

                with open(client_pub_key, "wb") as f:
                    f.write(client["public_key"].encode("utf-8")) 

                try: 
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
                        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=client_pub_key)
                        context.load_cert_chain(certfile=self.pub_key, keyfile=self.priv_key)

                        with context.wrap_socket(sock, server_side=False, server_hostname="rick.local") as secure_sock: 
                            secure_sock.connect((client["client_ip"], self.port))
            
                            try: 
                                secure_sock.send(str.encode(json.dumps({
                                    "message": message,
                                    "client_name": self.name 
                                })))
                            
                            except ConnectionResetError: 
                                print(Fore.RED + f"[-] - Sender | Connection Reset." + Style.RESET_ALL)
                                
                            try: 
                               data =secure_sock.recv(4096).decode()
                            except ssl.SSLError: 
                                print(Fore.RED + f"[-] Sender | Buffer Recieve Error." + Style.RESET_ALL)
                                continue


                            print(Fore.MAGENTA + f"[+] - Sender | Sent {message} and {client['client_name']}@{client['client_ip']} replied: {data}"  + Style.RESET_ALL)
                            
                            secure_sock.close()
                            self.connected_clients.append(client)
                            break 

                except ssl.SSLCertVerificationError or ssl.SSLError:
                    print(Fore.RED + f"[-] Sender | SSL Verification Error." + Style.RESET_ALL)
                    continue 

                self.connected_clients.append(client)

    def recieve(self): 
        """ Method to recieve message from another client. """


        client_pub_key = f"read-{self.pub_key}"


        with socket.socket() as bindsocket: 
            try: 
                bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                bindsocket.bind(("0.0.0.0", self.port))
                bindsocket.listen(5)
            except OSError:
                print(Fore.RED + f"[-] Reciever | Could not bind port {self.port}." + Style.RESET_ALL)
                return null 

            while True:
                self.get_client_list()

                for client in self.clients: 
                    if client["client_name"] != self.name:

                        try: 
                            with open(client_pub_key, "wb") as f: f.write(client["public_key"].encode("utf-8")) 

                            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                            context.verify_mode = ssl.CERT_REQUIRED
                            context.load_cert_chain(certfile=self.pub_key, keyfile=self.priv_key)
                            context.load_verify_locations(cafile=client_pub_key)
                            context.options |= ssl.OP_NO_TLSv1
                            context.options |= ssl.OP_NO_TLSv1_1
                            context.options |= ssl.OP_NO_TLSv1_2

                            
                            print(Fore.CYAN + "[+] Reciever ready for connections."  + Style.RESET_ALL)
                            newsocket, fromaddr = bindsocket.accept()

                            with context.wrap_socket(newsocket, server_side=True) as secure_sock: 
                                host, port = secure_sock.getpeername()

                                try:
                                    data = json.loads(secure_sock.recv(4096)) 
                                    print(Fore.BLUE + f"[+] Reciever | {data['client_name']}@{host} said: {data['message']}" + Style.RESET_ALL)
                                    secure_sock.send(str.encode("pong!"))
                                
                                finally:
                                    secure_sock.shutdown(socket.SHUT_RDWR)
                                    secure_sock.close()
                                        
                        except ssl.SSLError or ssl.SSLCertVerificationError:
                            #print(Fore.RED + f"[ERROR] Public key of {client} did not work." + Style.RESET_ALL)
                            continue 


if __name__ == "__main__":
    # change name and server address before running new client 
    client_runner = Client(name="client1", server="https://127.0.0.1:5000")

    sender    = multiprocessing.Process(target=client_runner.send)
    reciever  = multiprocessing.Process(target=client_runner.recieve)
    
    try:
        reciever.start()
        sender.start()

    except KeyboardInterrupt:
        exit(1)       



