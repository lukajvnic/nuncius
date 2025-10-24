import cli
from threading import Thread
import time
from datetime import datetime
from zoneinfo import ZoneInfo 


def main():
    username = "jvnic"
    online_users = 1

    cli.provide_session_information(username, online_users)

    thread = Thread(target=cli.start)
    thread.start()

    while True:
        time.sleep(5)
        timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M:%S")
        cli.provide_message("alice", timestamp, "whats up")


if __name__ == "__main__":
    main()

