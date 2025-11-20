import socket
import json
from threading import *
from constants import *
import copy
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = BIND_IPV4_ADDRESS
port = BIND_PORT
serversocket.bind((host, port))
serversocket.settimeout(1.0)

with open("users.json", "r") as file:
    users = json.loads(file.read())

clients = []
pubkeys = {}


class Client(Thread):
    def __init__(self, _socket, _address):
        Thread.__init__(self)
        self.sock = _socket
        self.addr = _address
        self.running = True
        self.username = None
        self.start()

    def run(self):
        while self.running:
            try:
                recv = self.sock.recv(8192).decode()

                try:
                    recieved = json.loads(recv)
                    if recieved.get("action") == "LOGOUT":
                        self.stop()
                    if recieved.get("action") == "LOGIN":
                        self.validate_login(recieved)
                except json.JSONDecodeError:
                    logging.error("garbage data received")
                    continue
            except:
                pass
        
    def validate_login(self, creds):
        username = creds.get("username")
        password = creds.get("password")
        pubkey = creds.get("pubkey")

        # update public keys dictionary
        pubkeys[username] = pubkey
        self.username = username

        response = {
            "pubkeys": pubkeys
        }

        if username in users and users[username]["password"] == password:
            response["status"] = 200  # ok
            logging.info(f"User {username} logged in successfully from {self.addr}")
            self.sock.send(bytes(json.dumps(response), "utf-8"))
            self.broadcast(username, pubkeys, "LOGIN")
        else:
            response["status"] = 401  # unauthorized
            logging.warning(f"Failed login attempt for user {username} from {self.addr}")

            self.sock.send(bytes(json.dumps(response), "utf-8"))
        # self.stop()
    
    def validate_logout(self):
        logging.info("user disconnected")
        self.broadcast(self.username, pubkeys, "LOGOUT")

    def broadcast(self, username, pubkeys, action):
        message = {
            "status": 200,
            "action": action,
            "username": username,
            "pubkeys": copy.deepcopy(pubkeys)
        }

        for client in clients:
            try:
                client.sock.send(bytes(json.dumps(message), "utf-8"))
            except Exception:
                pass  # client disconnected, ignore

    def stop(self):
        self.running = False
        pubkeys.pop(self.username, None)  # returns None if username not found as opposed to raising KeyError
        clients.remove(self)
        self.validate_logout()

        try:
            self.sock.close()
        except Exception:
            pass


def start_server():
    serversocket.listen(5)
    logging.info("Auth server - started & listening")
    try:
        while True:
            try:
                clientsocket, address = serversocket.accept()
                clients.append(Client(clientsocket, address))
            except Exception as e:
                pass  # timeout, continue listening
    finally:
        serversocket.close()


if __name__ == "__main__":
    start_server()
