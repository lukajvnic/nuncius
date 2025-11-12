import cli
from threading import Thread
import time
import login
from constants import *
import consumer


def main():
    auth = login.handle_login()
    if auth["status"] == 401:
        return

    cli.provide_session_information(auth["username"], 1)

    cli_thread = Thread(target=cli.start)
    cli_thread.start()
    consumer_thread = Thread(target=consumer.consume_messages, args=[cli])
    consumer_thread.start()

    while True:
        if not cli_thread.is_alive():
            print(f"[{APP_NAME}] {CLIENT_CLOSING_MESSAGE}")
            break


if __name__ == "__main__":
    main()
