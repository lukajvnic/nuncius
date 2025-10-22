import curses
import sys
from dataclasses import dataclass


'''
to continue:
 1. implement input area
 2. implement chat area
'''


@dataclass
class Session:
    stdscr: object
    username: str = "loading..."
    online_users: int = 0

    @property
    def header(self) -> str:
        return f"[ nuncius v0.1 -- {self.username} ] [ online -- {self.online_users} ] [ type -e to exit]"
    

def provide_session_information(session: Session, username: str, online_users: int):
    session.username = username
    session.online_users = online_users


def provide_message(session: Session, username: str, timestamp: str, message: str):
    formatted = f"[{timestamp}] {username}: {message}"
    ## session.chat.append_message(formatted)



def draw_header(session: Session):
    session.stdscr.addstr(0, 0, session.header)


def main(stdscr):
    curses.curs_set(0)
    session = Session(stdscr)

    start = time.time()

    while True:
        stdscr.clear()
        # h, w = stdscr.getmaxyx()
        draw_header(session)
        stdscr.refresh()


if __name__ == "__main__":
    try:
        sys.exit(curses.wrapper(main) or 0)
    except KeyboardInterrupt:
        pass
