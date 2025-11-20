from zoneinfo import ZoneInfo
from constants import *
import getpass
import socket
import json
import encryption
import keys
from datetime import datetime


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("172.22.144.1", 5431))
s.settimeout(5)


def get_username() -> str:
    return input(GET_USERNAME_MESSAGE).strip()


def get_password() -> str:
    return getpass.getpass(GET_PASSWORD_MESSAGE)


def authenticate(username: str, password: str, pubkey: encryption.Pubkey) -> int:
    payload = {
        "username": username,
        "password": password,
        "action": "LOGIN",
        "status": 200,
        "pubkey": {
            "n": pubkey.n,
            "e": pubkey.e
        }
    }

    s.send(bytes(json.dumps(payload), "utf-8"))
    recieved = json.loads(s.recv(RECV_BYTES).decode())

    return recieved


def listen(cli):
    while True:
        try:
            if cli.SESSION.killed:
                payload = {
                    "action": "LOGOUT",
                    "username": cli.SESSION.username,
                    "status": 200
                }
                s.send(bytes(json.dumps(payload), "utf-8"))
                break

            data = s.recv(RECV_BYTES).decode()
            if data:
                message = json.loads(data)
                if message.get("action") in ["LOGIN", "LOGOUT"]:
                    keys.update_pubkeys(message.get("pubkeys", {}))  # warning: this may overwrite existing keys
                    cli.provide_online_users(len(message.get("pubkeys", {})))
                    cli.provide_message("SYSTEM",
                                        datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M:%S"),
                                        f"User {message.get('username')} has logged {"in" if message.get("action") == "LOGIN" else "out"}.")
        except socket.timeout:
            continue


def handle_login(pubkey: encryption.Pubkey) -> dict:
    username = get_username()
    password = get_password()

    auth = authenticate(username, password, pubkey)
    status = auth.get("status")

    print(f"[{APP_NAME}] {LOGIN_SUCCESS_MESSAGE}" if status == 200 else f"[{APP_NAME}] {LOGIN_DENIED_MESSAGE}")

    # s.close()
    keys.update_pubkeys(auth.get("pubkeys", {}))

    return {
        "status": status,
        "username": username
    }

if __name__ == "__main__":
    handle_login()