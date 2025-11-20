import curses
import sys
from dataclasses import dataclass, field
from constants import *
from datetime import datetime
from zoneinfo import ZoneInfo 
import time
import producer


class Chat:
    def __init__(self):
        self.messages = []

    def write(self, message: str):
        if len(self.messages) >= CHAT_HISTORY_LENGTH:
            self.messages.pop(0)

        self.messages.append(message)
    
    def pull(self, num_lines: int) -> list[str]:
        return self.messages[-num_lines:]


@dataclass
class Session:
    stdscr: object = None
    username: str = "loading..."
    online_users: int = 0
    input_buffer: list[str] = field(default_factory=list)  # list not shared across instances
    chat: Chat = field(default_factory=Chat)

    killed: bool = False
    initialized = True

    def set_stdscr(self, stdscr):
        self.stdscr = stdscr

    @property
    def header(self) -> str:
        return f"[ {APP_NAME} v{VERSION} -- {self.username} ] [ online -- {self.online_users} ] [ type -e to exit]"


### START EXTERNAL FUNCTIONS ###


def provide_online_users(online_users: int):
    SESSION.online_users = online_users


def provide_session_information(username: str, online_users: int, maxlen: int):
    provide_online_users(online_users)
    SESSION.username = username
    SESSION.initialized = True
    SESSION.maxlen = maxlen


def provide_message(username: str, timestamp: str, message: str):
    SESSION.chat.write(f"[{timestamp}] {username}: {message}")


### END EXTERNAL FUNCTIONS ###


def draw_header():
    SESSION.stdscr.addstr(0, 0, SESSION.header)


def handle_input():
    try:
        ch = SESSION.stdscr.get_wch()  # get utf-8 character
    except curses.error:
        return False # no input, continue running

    if ch in ALLOWED_CHARS:  # regular character input
        SESSION.input_buffer.append(ch)
    elif isinstance(ch, str) and bytes(ch, 'utf-8') == b'\x08' and SESSION.input_buffer:  # backspace
        SESSION.input_buffer.pop()
    elif ch in ("\n", "\r") and SESSION.input_buffer:  # enter
        message = "".join(SESSION.input_buffer).strip()

        if message == "-e":
            return True  # trigger exit

        # provide_message(SESSION.username, datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M:%S"), message)
        producer.produce_message(SESSION.username, message, SESSION.maxlen)

        SESSION.input_buffer.clear()

    return False  # continue running


def draw_input():
    '''
    todo add line wrapping
    '''

    input_str = "".join(SESSION.input_buffer)
    y = curses.LINES - 1
    try:
        # clear the input line, draw prompt + text (clipped to screen width)
        SESSION.stdscr.move(y, 0)
        SESSION.stdscr.clrtoeol()
        SESSION.stdscr.addnstr(y, 0, f">{input_str}", curses.COLS - 1)

        # place the cursor at the end of what's being typed (stay within bounds)
        cur_x = min(1 + len(input_str), curses.COLS - 1)
        curses.curs_set(1)
        SESSION.stdscr.move(y, cur_x)
    except curses.error:
        # ignore drawing/move errors (resizes, etc.)
        pass


def draw_chat():
    chat_lines = curses.LINES - 2  # leave space for header + input line
    messages = SESSION.chat.pull(chat_lines)

    start_y = 1  # below header
    for i, message in enumerate(messages):
        y = start_y + i
        try:
            SESSION.stdscr.addnstr(y, 0, message, curses.COLS - 1)
        except curses.error:
            # ignore drawing errors (resizes, etc.)
            pass


def main(stdscr):
    SESSION.set_stdscr(stdscr)

    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)

    while not SESSION.initialized:
        time.sleep(0.1)

    while True:
        stdscr.clear()

        draw_chat()
        draw_header()
        draw_input()

        stdscr.refresh()

        exit = handle_input()

        if exit:
            SESSION.killed = True
            break

    return 0


SESSION = Session()

def start():
    try:
        sys.exit(curses.wrapper(main) or 0)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start()
