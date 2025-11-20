import cli
from threading import Thread
import time
import listener
from constants import *
import consumer
import encryption
import keys


def main():
    pubkey, privkey = encryption.generate_keypair()

    auth = listener.handle_login(pubkey)
    if auth["status"] != 200:
        return

    cli.provide_session_information(auth["username"], len(keys.get_pubkeys()), privkey.maxlen)

    cli_thread = Thread(target=cli.start)
    cli_thread.start()
    consumer_thread = Thread(target=consumer.consume_messages, args=[cli, privkey])
    consumer_thread.start()
    listener_thread = Thread(target=listener.listen, args=[cli])
    listener_thread.start()

    while True:
        if not cli_thread.is_alive():
            print(f"[{APP_NAME}] {CLIENT_CLOSING_MESSAGE}")
            break


if __name__ == "__main__":
    main()
