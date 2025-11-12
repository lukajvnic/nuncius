from constants import *
import getpass
import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.36.104.76", 5431))
s.settimeout(5)


def get_username() -> str:
    return input(GET_USERNAME_MESSAGE).strip()


def get_password() -> str:
    return getpass.getpass(GET_PASSWORD_MESSAGE)


def authenticate(username: str, password: str) -> int:
    payload = {
        "username": username,
        "password": password
    }

    s.send(bytes(json.dumps(payload), "utf-8"))
    recieved = json.loads(s.recv(RECV_BYTES).decode())

    return recieved.get("status")


def handle_login():
    username = get_username()
    password = get_password()

    auth = authenticate(username, password)
    print(f"[{APP_NAME}] {LOGIN_SUCCESS_MESSAGE}" if auth == 200 else f"[{APP_NAME}] {LOGIN_DENIED_MESSAGE}")

    s.close()

    return {
        "status": auth,
        "username": username
    }

if __name__ == "__main__":
    handle_login()