import socket
import json
from threading import *
import time
import copy
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.39.73.37"
port = 5431
serversocket.bind((host, port))
serversocket.settimeout(1.0)

with open("users.json", "r") as file:
    users = json.loads(file.read())

clients = []


class Client(Thread):
    def __init__(self, _socket, _address):
        Thread.__init__(self)
        self.sock = _socket
        self.addr = _address
        self.running = True
        self.start()

    def run(self):
        while self.running:
            print("aaaa")
            try:
                recv = self.sock.recv(8192).decode()

                try:
                    recieved = json.loads(recv)
                    self.validate_login(recieved)
                except json.JSONDecodeError:
                    logging.error("garbage data received")
                    continue
            except:
                pass
        
    def validate_login(self, creds):
        username = creds.get("username")
        password = creds.get("password")

        response = {}

        if username in users and users[username]["password"] == password:
            response["status"] = 200  # ok
            logging.info(f"User {username} logged in successfully from {self.addr}")
        else:
            response["status"] = 401  # unauthorized
            logging.warning(f"Failed login attempt for user {username} from {self.addr}")

        self.sock.send(bytes(json.dumps(response), "utf-8"))
        self.stop()
    
    def validate_logout(self):
        logging.info("user disconnected")
        pass

    def stop(self):
        self.running = False
        clients.remove(self)

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
